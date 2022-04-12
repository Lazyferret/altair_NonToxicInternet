let content = document.querySelectorAll('.pst')     //Получение комментариев на странице
let cleared_text = [];
content.forEach(function(item, i, arr) {
	cleared_text.push(content[i].textContent);      //Получение очищенного текста
});	
let data = JSON.stringify(cleared_text);            //Преобразование полученных данных в JSON
//console.log(data);
var xmlHttp = new XMLHttpRequest();
xmlHttp.open( "POST", 'http://localhost:2000', true ); // false for synchronous request
xmlHttp.send(data);

xmlHttp.onload = () => {
	resp = JSON.parse(xmlHttp.response)

	content.forEach(function(item, i, arr) {
		if (resp[i]=='1'){
		content[i].style.backgroundColor = "#FA8072";
		content[i].textContent="***********************************************************************"
		}
	});
}