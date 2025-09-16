// Connect WebSocket (port = HTTP port + 1)
const ws = new WebSocket("ws://" + location.hostname + ":" + (location.port*1 + 1));
const chat = document.getElementById("chat");
const msgInput = document.getElementById("msg");
const sendBtn = document.getElementById("send");

// Load nickname or ask
let nickname = localStorage.getItem("nickname");
if (!nickname) {
    nickname = prompt("Enter your nickname:") || "Anonymous";
    localStorage.setItem("nickname", nickname);
}

// Send join message when connected
ws.onopen = () => { ws.send(`${nickname} joined`); };

// Display messages
ws.onmessage = (event) => {
    const div = document.createElement("div");
    div.textContent = event.data;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
};

// Send message
function sendMessage(){
    if(msgInput.value.trim() !== ""){
        ws.send(`${nickname}: ${msgInput.value}`);
        msgInput.value = "";
    }
}

sendBtn.onclick = sendMessage;
msgInput.addEventListener("keypress", e => { if(e.key==="Enter") sendMessage(); });

// Send leave message before closing
window.addEventListener("beforeunload", ()=> ws.send(`${nickname} left`));