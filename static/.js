// 사용자가 Enter키 또는 버튼을 눌렀을 때 메시지 전송 처리
function sendMessage() {
    let message = document.getElementById("chat_input").value.trim();
    if (!message) {
        alert("메시지를 입력하세요.");
        return;
    }

    let chatContainer = document.querySelector(".chat-container");

    // 사용자 메시지 추가
    let userMessage = document.createElement("div");
    userMessage.className = "message right";
    userMessage.innerText = message;
    chatContainer.appendChild(userMessage);

    document.getElementById("chat_input").value = "";

    let xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/chat_message/" + message, true);

    xhr.onload = function () {
        if (xhr.status === 200) {
            // xhr.responseText: 응답받은 text
            // JSON.parse(json 문자열): json을 JS 객체로 변환
            // "{response:'안녕하세요'}" => {response:"안녕하세요"}
            let data = JSON.parse(xhr.responseText);
            let chatContainer = document.querySelector(".chat-container");
            let aiMessage = document.createElement("div");
            aiMessage.className = "left";
            aiMessage.innerHTML = `
            <img src="static/media/images/Isabelle.jpg" width="40px" class="rounded-circle mb-10">
            <div class="message ai">${data.response}</div>
            `;
            chatContainer.appendChild(aiMessage);

            chatContainer.scrollTop = chatContainer.scrollHeight;
            
        } else {
            alert(`Error code: ${xhr.status}, Error Msg: ${xhr.statusText}`);
        }
    };
    // 서버로 요청
    // xhr.open() 설정에 맞춰 요청
    // 응답이 오면 xhr.onload의 callback이 호출되어 응답 데이터 처리

    xhr.send();
}


// 버튼 클릭 및 Enter 키 이벤트에 이벤트 리스너 등록
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
