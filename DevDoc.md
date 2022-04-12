# Документация разработчика
Запуск прокта ->

1. Добавить главную папку проекта в расширения Chrome
2. Запустить main.py

Отправка запроса JS ->
```javascript
var xmlHttp = new XMLHttpRequest();
xmlHttp.open( "POST", 'http://localhost:2000', true ); // false for synchronous request
xmlHttp.send(data);
```
