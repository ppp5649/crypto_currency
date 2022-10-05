// socket.readyState 값은 CONNECTING, 연결이 성공하면 OPEN으로 변경됨
// ws는 http를 대체함
var socket = new WebSocket('ws://localhost:8000/ws/main/')

socket.onmessage = function(e){
    var djangoData = JSON.parse(e.data); // JSON.parse : str을 json 으로 변환
    console.log(djangoData); // json 형태로 데이터를 넘겨줌
    document.querySelector('#app1').innerText = djangoData.value1;
    document.querySelector('#app2').innerText = djangoData.value2;
}