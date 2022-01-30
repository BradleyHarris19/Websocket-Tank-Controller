let lightState 
let stateindicator = document.querySelector('.state')
let redbutton = document.querySelector('.red')
let greenbutton = document.querySelector('.green')
let defultbuttonbackground = 'rgb(236, 236, 236)'

websocket = new WebSocket("ws://127.0.0.1:6789/");

websocket.onopen = function(e) {
    stateindicator.innerHTML = 'Connection established';
    stateindicator.style.backgroundColor = 'green';
};

document.querySelector('.red').onclick = function (event) {
    lightState.red = !lightState.red
    websocket.send(JSON.stringify(lightState));
    if (lightState.red){
        redbutton.style.backgroundColor = '#ff000030';
    } else {
        redbutton.style.backgroundColor = defultbuttonbackground
    }
    console.log(lightState);
}

document.querySelector('.green').onclick = function (event) {
    lightState.green = !lightState.green
    websocket.send(JSON.stringify(lightState));
    if (lightState.green){
        greenbutton.style.backgroundColor = '#00900030';
    } else {
        greenbutton.style.backgroundColor = defultbuttonbackground
    }
    console.log(lightState);
}

websocket.onmessage = function(event) {
    lightState = JSON.parse(event.data);
    console.log(lightState);
};

websocket.onerror = function(error) {
    alert(`[error] ${error.message}`);
};

websocket.onclose = function(e) {
    stateindicator.innerHTML = 'Connection closed';
    stateindicator.style.backgroundColor = 'red';
};