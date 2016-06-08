var data = {a:1, b:2, c:3};
var json = JSON.stringify(data);
var blob = new Blob([json], {type: "application/json"});
var url  = URL.createObjectURL(blob);

var a = document.createElement('a');
a.download    = "backup.json";
a.href        = url;
a.textContent = "Download backup.json";

document.getElementById('content').appendChild(a);

function test(){
  alert("s");
}
