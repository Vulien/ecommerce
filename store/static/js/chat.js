document.addEventListener("DOMContentLoaded", function () {
    // Lấy các phần tử cần thiết từ DOM
    const chatIcon = document.getElementById("chat-icon");
    const chatContainer = document.getElementById("chat-container");
    const chatHeader = document.getElementById("chat-header");
    const chatBox = document.getElementById("chat-box");
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");
    const isAuthenticated = document.getElementById("user-authenticated").textContent.trim() === "true";
    const userId = document.getElementById("user-id").textContent.trim();

    // Khi bấm vào biểu tượng chat:
    chatIcon.addEventListener("click", function () {
        if (!isAuthenticated) {
            alert("Vui lòng đăng nhập bằng tài khoản email để chat!");
            window.location.href = "/login/";  // Điều chỉnh URL đăng nhập nếu cần
        } else {
            // Nếu đã đăng nhập, toggle hiển thị hộp chat
            chatContainer.style.display = (chatContainer.style.display === "none") ? "block" : "none";
        }
    });

    // Ngoài ra, nếu bấm vào tiêu đề hộp chat, cũng toggle hiển thị nội dung chat
    chatHeader.addEventListener("click", function () {
        chatContainer.style.display = (chatContainer.style.display === "none") ? "block" : "none";
    });

    // Chỉ thiết lập WebSocket nếu người dùng đã đăng nhập
    if (isAuthenticated) {
        const ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
        // Kết nối tới đường dẫn WebSocket; đảm bảo cấu hình Channels của bạn có endpoint "/ws/chat/"
        const socket = new WebSocket(ws_scheme + "://" + window.location.host + "/ws/chat/");

        socket.onopen = function () {
            console.log("Kết nối WebSocket thành công!");
        };

        socket.onmessage = function (event) {
            const data = JSON.parse(event.data);
            const messageElement = document.createElement("p");
            messageElement.innerHTML = `<strong>${data.sender}:</strong> ${data.message}`;
            chatBox.appendChild(messageElement);
            chatBox.scrollTop = chatBox.scrollHeight;
        };

        socket.onerror = function (error) {
            console.error("Lỗi WebSocket:", error);
        };

        // Gửi tin nhắn khi bấm nút hoặc nhấn Enter
        sendButton.addEventListener("click", sendMessage);
        messageInput.addEventListener("keypress", function (e) {
            if (e.key === "Enter") {
                sendMessage();
            }
        });

        function sendMessage() {
            const message = messageInput.value.trim();
            if (message !== "") {
                // Giả sử admin có ID cố định = 1; nếu bạn có logic khác, hãy thay đổi cho phù hợp
                socket.send(JSON.stringify({
                    "receiver_id": 1,
                    "message": message
                }));
                messageInput.value = "";
            }
        }
    }
});
