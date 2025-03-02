document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const messageInput = document.getElementById("message-input");
    const chatForm = document.getElementById("chat-form");
    const receiverEmail = document.getElementById("receiver-email").value;

    if (!chatBox || !messageInput || !chatForm || !receiverEmail) return;

    const socket = new WebSocket(`ws://${window.location.host}/ws/chat/${receiverEmail}/`);

    socket.onopen = function () {
        console.log("WebSocket connected!");
    };

    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        chatBox.innerHTML += `<p><strong>${data.sender}:</strong> ${data.message}</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    chatForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const message = messageInput.value.trim();
        if (message !== "") {
            socket.send(JSON.stringify({
                "message": message
            }));
            messageInput.value = "";
        }
    });
});
