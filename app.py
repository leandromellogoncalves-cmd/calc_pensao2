from flask import Flask, render_template, request
from decimal import Decimal, InvalidOperation

app = Flask(__name__)
SALARIO_MINIMO_2026 = Decimal("1621.00")

def money(v):
    try:
        raw = str(v or "0").strip()
        if "," in raw:
            raw = raw.replace(".", "").replace(",", ".")
        return Decimal(raw or "0")
    except (InvalidOperation, ValueError):
        return Decimal("0")

def fmt(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def collect_rows(form, prefix):
    names = form.getlist(f"{prefix}_name")
    values = form.getlist(f"{prefix}_value")
    rows = []
    for name, value in zip(names, values):
        val = money(value)
        if name.strip() or val:
            rows.append({"name": name.strip() or "Verba", "value": val})
    return rows

def totals(form):
    vencimentos = collect_rows(form, "venc")
    previdencia = collect_rows(form, "prev")
    irrf = collect_rows(form, "irrf")
    bruto = sum((r["value"] for r in vencimentos), Decimal("0"))
    prev = sum((r["value"] for r in previdencia), Decimal("0"))
    irrf_total = sum((r["value"] for r in irrf), Decimal("0"))
    liquido = bruto - prev - irrf_total
    dependentes = int(form.get("dependentes", 0) or 0)
    percentual = money(form.get("percentual", 0))
    salario_minimo = money(form.get("salario_minimo", SALARIO_MINIMO_2026))
    return {
        "vencimentos": vencimentos, "previdencia": previdencia, "irrf": irrf,
        "bruto": bruto, "prev": prev, "irrf_total": irrf_total, "liquido": liquido,
        "dependentes": dependentes, "percentual": percentual,
        "salario_minimo": salario_minimo
    }

def memory_lines(data, tipo, base, valor):
    p = data["percentual"]
    lines = []
    lines.append(("Vencimentos", " + ".join([f'{r["name"]}: {fmt(r["value"])}' for r in data["vencimentos"]]) or "Nenhuma verba"))
    lines.append(("Total bruto", fmt(data["bruto"])))
    lines.append(("Previdência", " + ".join([f'{r["name"]}: {fmt(r["value"])}' for r in data["previdencia"]]) or "Nenhum desconto"))
    lines.append(("Total previdência", fmt(data["prev"])))
    lines.append(("IRRF", " + ".join([f'{r["name"]}: {fmt(r["value"])}' for r in data["irrf"]]) or "Nenhum desconto"))
    lines.append(("Total IRRF", fmt(data["irrf_total"])))
    lines.append(("Líquido apurado", f'{fmt(data["bruto"])} - {fmt(data["prev"])} - {fmt(data["irrf_total"])} = {fmt(data["liquido"])}'))
    lines.append(("Dependentes informados", str(data["dependentes"])))
    lines.append(("Percentual da pensão", f"{p}%"))
    if tipo == "liquido":
        formula = f"{fmt(base)} × {p}% = {fmt(valor)}"
    elif tipo == "bruto":
        formula = f"{fmt(base)} × {p}% = {fmt(valor)}"
    else:
        formula = f"{fmt(base)} × {p}% = {fmt(valor)}"
    lines.append(("Base escolhida", f"{tipo} → {fmt(base)}"))
    lines.append(("Fórmula final", formula))
    lines.append(("Resultado", fmt(valor)))
    return lines

def calc_normal(data, tipo):
    pct = data["percentual"] / Decimal("100")
    if tipo == "liquido":
        base = data["liquido"]
        nome = "Pensão sobre o líquido"
        chave = "liquido"
    elif tipo == "bruto":
        base = data["bruto"]
        nome = "Pensão sobre o bruto"
        chave = "bruto"
    else:
        base = data["salario_minimo"]
        nome = "Pensão sobre o salário mínimo"
        chave = "salario_minimo"
    valor = max(Decimal("0"), base * pct)
    return {"tipo": nome, "base": base, "valor": valor,
            "memoria": memory_lines(data, chave, base, valor)}

def reverse_calc(data, pensao):
    pct = data["percentual"] / Decimal("100")
    candidatos = []
    if pct > 0:
        candidatos = [
            ("Pensão sobre o líquido", data["liquido"], data["liquido"] * pct),
            ("Pensão sobre o bruto", data["bruto"], data["bruto"] * pct),
            ("Pensão sobre o salário mínimo", data["salario_minimo"], data["salario_minimo"] * pct),
        ]
    matches = [c for c in candidatos if abs(c[2] - pensao) <= Decimal("0.01")]
    if matches:
        escolhido = matches[0]
        status = "Correspondência encontrada considerando diferença máxima de R$ 0,01."
    else:
        escolhido = min(candidatos, key=lambda c: abs(c[2] - pensao)) if candidatos else ("Indefinido", Decimal("0"), Decimal("0"))
        status = "Não houve correspondência exata; a modalidade abaixo é a mais próxima."

    memoria = []
    for tipo, base, calculado in candidatos:
        diferenca = abs(calculado - pensao)
        memoria.append({
            "tipo": tipo, "base": base, "calculado": calculado, "diferenca": diferenca,
            "formula": f"{fmt(base)} × {data['percentual']}% = {fmt(calculado)}"
        })
    base_reversa = (pensao / pct) if pct > 0 else Decimal("0")
    return {
        "escolhido": {"tipo": escolhido[0], "base": escolhido[1], "calculado": escolhido[2]},
        "candidatos": candidatos, "memoria": memoria, "status": status,
        "base_reversa": base_reversa
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/normal", methods=["GET", "POST"])
def normal():
    result = None
    data = {"bruto": Decimal("0"), "prev": Decimal("0"), "irrf_total": Decimal("0"),
            "liquido": Decimal("0"), "dependentes": 0, "percentual": Decimal("0"),
            "salario_minimo": SALARIO_MINIMO_2026, "vencimentos": [], "previdencia": [], "irrf": []}
    if request.method == "POST":
        data = totals(request.form)
        result = calc_normal(data, request.form.get("tipo", "liquido"))
    return render_template("normal.html", data=data, result=result, fmt=fmt)

@app.route("/reversa", methods=["GET", "POST"])
def reversa():
    result = None
    data = {"bruto": Decimal("0"), "prev": Decimal("0"), "irrf_total": Decimal("0"),
            "liquido": Decimal("0"), "dependentes": 0, "percentual": Decimal("0"),
            "salario_minimo": SALARIO_MINIMO_2026, "vencimentos": [], "previdencia": [], "irrf": []}
    pensao = Decimal("0")
    if request.method == "POST":
        data = totals(request.form)
        pensao = money(request.form.get("pensao"))
        result = reverse_calc(data, pensao)
    return render_template("reversa.html", data=data, pensao=pensao, result=result, fmt=fmt)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
