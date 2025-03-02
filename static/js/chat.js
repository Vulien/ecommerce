document.addEventListener("DOMContentLoaded", function () {
    const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/");
    const chatBox = document.getElementById("chat-box");

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);

        // Nếu nhận được lịch sử tin nhắn
        if (data.history) {
            chatBox.innerHTML = "";  // Xóa nội dung cũ
            data.history.forEach(msg => {
                addMessageToChatBox(msg.sender_id, msg.message);
            });
        } else {
            // Nếu nhận được tin nhắn mới
            addMessageToChatBox(data.sender_id, data.message);
        }
    };

    chatSocket.onclose = function (e) {
        console.error("Chat socket closed unexpectedly");
    };

    document.getElementById("send-button").onclick = function () {
        const messageInput = document.getElementById("message-input");
        const receiverId = document.getElementById("receiver-id").value;

        chatSocket.send(JSON.stringify({
            "message": messageInput.value,
            "receiver_id": receiverId
        }));
        messageInput.value = "";
    };

    function addMessageToChatBox(senderId, message) {
        const p = document.createElement("p");
        p.innerHTML = `<strong>${senderId}:</strong> ${message}`;
        chatBox.appendChild(p);
        chatBox.scrollTop = chatBox.scrollHeight;  // Cuộn xuống tin nhắn mới nhất
    }
});
