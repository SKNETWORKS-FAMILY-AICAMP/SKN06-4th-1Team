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

            saveChatHistory(message, data.response);
            
        } else {
            alert(`Error code: ${xhr.status}, Error Msg: ${xhr.statusText}`);
        }
    };
    // 서버로 요청
    // xhr.open() 설정에 맞춰 요청
    // 응답이 오면 xhr.onload의 callback이 호출되어 응답 데이터 처리

    xhr.send();
}


// 대화 저장 함수
function saveChatHistory(userMessage, aiMessage) {
    let chatHistory = JSON.parse(localStorage.getItem("chatHistory")) || [];
    let now = new Date();
    let chatEntry = {
        date: now.toISOString().split("T")[0], // YYYY-MM-DD 형식
        user: userMessage,
        ai: aiMessage,
    };

    chatHistory.push(chatEntry);
    
    // 한 달 이상 지난 대화 삭제
    let oneMonthAgo = new Date();
    oneMonthAgo.setMonth(oneMonthAgo.getMonth() - 1);
    chatHistory = chatHistory.filter(chat => new Date(chat.date) >= oneMonthAgo);

    localStorage.setItem("chatHistory", JSON.stringify(chatHistory));

    // 사이드바 업데이트
    updateChatSidebar();
}

// 사이드바에 대화 목록 표시
function updateChatSidebar() {
    let chatHistory = JSON.parse(localStorage.getItem("chatHistory")) || [];
    let chatList = document.getElementById("chat-history-list");
    chatList.innerHTML = "";

    chatHistory.forEach((chat, index) => {
        let listItem = document.createElement("li");
        listItem.textContent = `${chat.date} - ${chat.user.slice(0, 15)}...`; // 제목을 간단히 요약
        listItem.onclick = () => loadChat(index);
        chatList.appendChild(listItem);
    });
}

// 대화 기록 불러오기
function loadChat(index) {
    let chatHistory = JSON.parse(localStorage.getItem("chatHistory")) || [];
    if (chatHistory[index]) {
        let chatContainer = document.querySelector(".chat-container");
        chatContainer.innerHTML = "";

        let userMessage = document.createElement("div");
        userMessage.className = "message right";
        userMessage.innerText = chatHistory[index].user;
        chatContainer.appendChild(userMessage);

        let aiMessage = document.createElement("div");
        aiMessage.className = "message left";
        aiMessage.innerText = chatHistory[index].ai;
        chatContainer.appendChild(aiMessage);
    }
}

// 대화 기록 불러오기
function loadChatHistory() {
    updateChatSidebar();
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
