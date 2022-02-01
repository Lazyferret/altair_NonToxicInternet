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

xmlHttp.onload = () => {
	resp = xmlHttp.response

	content.forEach(function(item, i, arr) {
		if (resp[i]=='тест'){
		content[i].style.backgroundColor = "#FA8072";
		}
	});
}