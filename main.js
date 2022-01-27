let content = document.querySelectorAll('.pst')
//let cleared_text = $(content).contents().eq(1).text();
let cleared_text = [];
content.forEach(function(item, i, arr) {
	cleared_text.push(content[i].textContent);
});	
let data = JSON.stringify(cleared_text);
//console.log(data);
var xmlHttp = new XMLHttpRequest();
xmlHttp.open( "POST", 'http://localhost:2000', true ); // false for synchronous request
xmlHttp.send(data);

//var xmlHttp2 = new XMLHttpRequest();
//xmlHttp2.open( "POST", 'http://localhost:2000', true ); // false for synchronous request
//xmlHttp2.send(data);
//var recieved = JSON.parse(xmlHttp.response);
console.log(xmlHttp.response);
//recieved.forEach(function(item, i, arr) {
//	console.log(recieved[i]);
//});	