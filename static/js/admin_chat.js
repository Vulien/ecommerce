document.addEventListener("DOMContentLoaded", function () {
    const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/");
    const chatBox = document.getElementById("chat-box");
    const customerSelect = document.getElementById("customer-select");

    let selectedCustomerId = customerSelect.value;

    customerSelect.addEventListener("change", function () {
        selectedCustomerId = this.value;
        loadChatHistory(selectedCustomerId);
    });

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);

        if (data.history) {
            chatBox.innerHTML = "";
            data.history.forEach(msg => {
                addMessageToChatBox(msg.sender_id, msg.message);
            });
        } else {
            addMessageToChatBox(data.sender_id, data.message);
        }
    };

    document.getElementById("send-button").onclick = function () {
        const messageInput = document.getElementById("message-input");

        chatSocket.send(JSON.stringify({
            "message": messageInput.value,
            "receiver_id": selectedCustomerId
        }));
        messageInput.value = "";
    };

    function addMessageToChatBox(senderId, message) {
        const p = document.createElement("p");
        p.innerHTML = `<strong>${senderId}:</strong> ${message}`;
        chatBox.appendChild(p);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function loadChatHistory(userId) {
        chatSocket.send(JSON.stringify({
            "load_history": true,
            "user_id": userId
        }));
    }

    loadChatHistory(selectedCustomerId);
});
