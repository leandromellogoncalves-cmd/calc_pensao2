# Sistema Web de Calculo de Pensao

Aplicacao web em Python + Flask para calculo de pensao normal e reversa.

## Funcionalidades

- Tela inicial com dois botoes: Calculo Normal e Calculo Reverso.
- Lancamento de varias verbas de vencimento.
- Lancamento separado de previdencia e IRRF.
- Campo de dependentes.
- Campo de percentual da pensao.
- Tres modalidades:
  1. Pensao sobre o liquido
  2. Pensao sobre o bruto
  3. Pensao sobre o salario minimo
- Calculo reverso: informa-se o valor da pensao e o sistema compara as tres modalidades e identifica a correspondencia exata, quando houver.
- Exibe a base utilizada, tipo de calculo, percentual e memoria de calculo.
- Salario minimo padrao de R$ 1.621,00 para 2026, podendo ser alterado no formulario.

## Formula usada nesta versao

Bruto = soma das verbas de vencimento.

Liquido = Bruto - Previdencia - IRRF.

Pensao sobre liquido = Liquido x percentual / 100.

Pensao sobre bruto = Bruto x percentual / 100.

Pensao sobre salario minimo = Salario minimo x percentual / 100.

### Observacao importante

O sistema nao calcula automaticamente INSS ou IRRF. O usuario informa os valores desses descontos, pois a base juridica da pensao pode variar conforme a decisao judicial, acordo ou titulo executivo. Dependentes ficam registrados no calculo, mas nao alteram o IRRF automaticamente nesta versao.

## Como executar no Windows

1. Instale Python 3.11 ou superior.
2. Abra o Prompt de Comando na pasta do projeto.
3. Execute:

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    python app.py

4. Acesse no navegador:

    http://127.0.0.1:5000

## Estrutura

app.py
requirements.txt
templates/
  index.html
  normal.html
  reversa.html
static/
  style.css
  app.js


## Inicialização com dois cliques

Depois de configurar o ambiente virtual e instalar as dependências pela primeira vez,
você pode iniciar o sistema simplesmente executando:

    INICIAR_SISTEMA.bat

O arquivo abre automaticamente o navegador e inicia o servidor Flask.

## Memória de cálculo

A interface agora apresenta:
- composição das verbas de vencimento;
- total bruto;
- composição dos descontos previdenciários;
- total de previdência;
- composição do IRRF;
- total de IRRF;
- líquido apurado;
- dependentes informados;
- percentual;
- base selecionada;
- fórmula aplicada;
- resultado final.

No cálculo reverso, o sistema ainda compara as três modalidades e informa a diferença
entre o valor informado e o valor calculado em cada hipótese.
