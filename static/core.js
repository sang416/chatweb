const socket = io();

const chat = document.getElementById('chat');
const sendButton = document.getElementById('send');
const nicknameInput = document.getElementById('nickname');
const messageInput = document.getElementById('message');

// 메시지 보내기 함수
function sendMessage() {
    const nickname = nicknameInput.value.trim();
    const message = messageInput.value.trim();
    if (nickname && message) {
        socket.send({ nickname, message });
        messageInput.value = ''; // 메시지 입력 필드 초기화
    }
}

// "Send" 버튼 클릭 시 메시지 전송
sendButton.addEventListener('click', sendMessage);

// "Enter" 키 입력 시 메시지 전송
messageInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        event.preventDefault(); // 기본 Enter 동작(줄 바꿈) 방지
        sendMessage();
    }
});

// 메시지 수신
socket.on('message', (data) => {
    const div = document.createElement('div');
    div.innerHTML = `<strong>${data.timestamp} [${data.nickname}]:</strong> ${data.message}`;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
});
