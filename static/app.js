document.addEventListener("click", function(e){
  if(e.target.matches(".add")){
    const target=document.getElementById(e.target.dataset.target);
    const p=e.target.dataset.prefix;
    const row=document.createElement("div");
    const nameField=p==="venc"?"venc_name":p==="prev"?"prev_name":"irrf_name";
    const valueField=p==="venc"?"venc_value":p==="prev"?"prev_value":"irrf_value";
    row.className="row";
    row.innerHTML=`<input name="${nameField}" placeholder="Descrição da verba"><input name="${valueField}" type="number" step="0.01" placeholder="0,00"><button type="button" class="remove">×</button>`;
    target.appendChild(row);
  }
  if(e.target.matches(".remove")){
    const row=e.target.closest(".row");
    const parent=row.parentElement;
    if(parent.children.length>1) row.remove();
    else row.querySelectorAll("input").forEach(i=>i.value="");
  }
});