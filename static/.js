function sendMessage() {
    let message = document.getElementById("chat_input").value;
    if (!message) {
        alert("메시지를 입력하세요.");
        return;
    }

    let xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/chat_message/" + message, true);

    xhr.onload = function () {
        if (xhr.status === 200) {
            // xhr.responseText: 응답받은 text
            // JSON.parse(json 문자열): json을 JS 객체로 변환
            // "{response:'안녕하세요'}" => {response:"안녕하세요"}
            let data = JSON.parse(xhr.responseText);
            let chatContainer = document.querySelector(".chat-container");
            let userMessage = document.createElement("div");
            userMessage.className = "message right";
            userMessage.innerText = message;
            chatContainer.appendChild(userMessage);

            let aiMessage = document.createElement("div");
            aiMessage.className = "message left";
            aiMessage.innerText = data.response;
            chatContainer.appendChild(aiMessage);

            document.getElementById("chat_input").value = "";
        } else {
            alert(Error code: ${xhr.status}, Error Msg: ${xhr.statusText});
        }
    };
    // 서버로 요청
    // xhr.open() 설정에 맞춰 요청
    // 응답이 오면 xhr.onload의 callback이 호출되어 응답 데이터 처리

    xhr.send();
}

document
    .getElementById("send_btn")
    .addEventListener("click", sendMessage);
document
    .getElementById("chat_input")
    .addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
        sendMessage();
        }
});
