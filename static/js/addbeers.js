const user_username = document.body.dataset.username;
const ws_url = document.body.dataset.ws_url
const ws = new WebSocket(`${ws_url}/dashboard/${user_username}`);
   
    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        document.getElementById("cl33").innerText = data.cl33;
        document.getElementById("cl50").innerText = data.cl50;
        document.getElementById("jarra_caña").innerText = data.jarra_caña;
        document.getElementById("total_beers").innerText = data.total_beers;
    };
    
    function send(tipo) {
        cl_33 = document.getElementById("cl33").innerText
        cl_50 = document.getElementById("cl50").innerText
        jarra_caña = document.getElementById("jarra_caña").innerText
        total_beers = document.getElementById("total_beers").innerText
        
        if (ws.readyState === WebSocket.OPEN && cl_33 > -1 && cl_50 > -1 && jarra_caña > -1 && total_beers > -1) {
            ws.send(tipo);
        }
    }