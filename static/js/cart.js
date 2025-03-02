document.addEventListener("DOMContentLoaded", function() {
    let cartMessage = document.getElementById("cart-message");

    // Xử lý thêm vào giỏ hàng
    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", function() {
            let productId = this.getAttribute("data-product");
            let csrftoken = getCSRFToken();

            fetch("/add-to-cart/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken
                },
                body: JSON.stringify({ "product_id": productId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.cart_count !== undefined) {
                    document.getElementById("cart-count").textContent = data.cart_count;
                    showMessage("Sản phẩm đã được thêm vào giỏ hàng!", "success");
                }
            })
            .catch(error => console.error("Lỗi:", error));
        });
    });

    // Xử lý xóa sản phẩm (dùng event delegation)
    document.body.addEventListener("click", function(event) {
        if (event.target.classList.contains("remove-from-cart")) {
            let productId = event.target.getAttribute("data-product");

            fetch(`/remove-from-cart/${productId}/`, { method: "POST" })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showMessage("Sản phẩm đã được xoá khỏi giỏ hàng!", "danger");
                    window.location.reload();  // Load lại trang để cập nhật giỏ hàng
                }
            })
            .catch(error => console.error("Lỗi:", error));
        }
    });

    // Hàm hiển thị thông báo
    function showMessage(message, type) {
        cartMessage.textContent = message;
        cartMessage.className = `alert alert-${type}`;
        cartMessage.classList.remove("d-none");

        setTimeout(() => {
            cartMessage.classList.add("d-none");
        }, 2000);
    }

    // Hàm lấy CSRF token
    function getCSRFToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            let cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.startsWith("csrftoken=")) {
                    cookieValue = cookie.substring("csrftoken=".length, cookie.length);
                    break;
                }
            }
        }
        return cookieValue;
    }
});

document.addEventListener("DOMContentLoaded", function () {
    fetch("/chat-history/")
        .then(response => response.json())
        .then(data => {
            const chatBox = document.getElementById("chat-box");
            data.messages.forEach(msg => {
                const messageElement = document.createElement("div");
                messageElement.textContent = `${msg.sender}: ${msg.message}`;
                chatBox.appendChild(messageElement);
            });
        });
});
