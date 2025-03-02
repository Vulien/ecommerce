document.addEventListener("DOMContentLoaded", function () {
    // Xử lý thêm sản phẩm vào giỏ hàng
    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", function () {
            let productId = this.getAttribute("data-product");
            let quantityInputId = this.getAttribute("data-quantity-input");
            let quantity = document.getElementById(quantityInputId).value;
            let csrftoken = getCSRFToken();

            fetch("/add-to-cart/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken
                },
                body: JSON.stringify({ "product_id": productId, "quantity": quantity })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.cart_count !== undefined) {
                        updateCartCount(data.cart_count);
                        showMessage("Sản phẩm đã được thêm vào giỏ hàng!", "success");
                    }
                })
                .catch(error => console.error("Lỗi:", error));
        });
    });

    // Xử lý xoá sản phẩm khỏi giỏ hàng
    document.querySelectorAll(".remove-from-cart").forEach(button => {
        button.addEventListener("click", function () {
            let productId = this.getAttribute("data-product");
            let csrftoken = getCSRFToken();

            fetch(`/remove-from-cart/${productId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrftoken
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showMessage("Sản phẩm đã được xoá khỏi giỏ hàng!", "danger");
                        // Xoá dòng sản phẩm khỏi giao diện
                        let productRow = document.getElementById(`cart-item-${productId}`);
                        if (productRow) {
                            productRow.remove();
                        }

                        let cartSubtotal = document.getElementById("cart-subtotal");
                        if (cartSubtotal) {
                            cartSubtotal.textContent = parseFloat(data.total_price).toFixed(2);
                        }
                        // Cập nhật lại số lượng giỏ hàng nếu có
                        let cartCountElement = document.getElementById("cart-count");
                        if (cartCountElement) {
                            cartCountElement.textContent = data.cart_count;
                        }
                    }
                })
                .catch(error => console.error("Lỗi:", error));
        });
    });


    // Xử lý sự kiện cho nút "Close" bên trong overlay
    document.querySelectorAll(".close-desc").forEach(button => {
        button.addEventListener("click", function () {
            // Tìm overlay cha của nút này và ẩn nó
            let overlay = this.closest(".desc-overlay");
            overlay.style.display = "none";
            // Cập nhật lại text của "See more" tương ứng
            let cardBody = this.closest(".card-body");
            let seeMoreLink = cardBody.querySelector(".see-more");
            if (seeMoreLink) {
                seeMoreLink.textContent = "See more";
            }
        });
    });

    // Đặt hàm removeFromCart vào phạm vi toàn cục (ví dụ: gắn lên window)
    window.removeFromCart = function (productId) {
        let csrftoken = getCSRFToken();
        fetch(`/remove-from-cart/${productId}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateCartCount(data.cart_count);
                    updateMiniCart();

                    // Nếu trang cart.html cũng cập nhật qua AJAX, gọi hàm cập nhật tại đây:
                    if (typeof updateCartPage === "function") {
                        updateCartPage();
                    }
                    showMessage("Sản phẩm đã được xoá khỏi giỏ hàng!", "danger");
                } else {
                    console.error("Xoá sản phẩm thất bại:", data.error);
                }
            })
            .catch(error => console.error("Lỗi xoá sản phẩm:", error));
    };

    document.getElementById("mini-cart-content").addEventListener("click", function (e) {
        const btn = e.target.closest(".remove-from-cart");
        if (btn) {
            let productId = btn.getAttribute("data-product");
            removeFromCart(productId);
        }
    });



    function updateMiniCart() {
        fetch(getCartUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error("HTTP error " + response.status);
                }
                return response.json();
            })
            .then(data => {
                let contentDiv = document.getElementById("mini-cart-content");
                if (data.cart_items && data.cart_items.length > 0) {
                    let html = '<ul class="list-group">';
                    data.cart_items.forEach(item => {
                        html += `<li class="list-group-item">
                        <div class="row align-items-center">
                          <div class="col-3">
                            ${item.image_url ? `<img src="${item.image_url}" alt="${item.name}" class="img-fluid">` : `<img src="{% static 'images/default.png' %}" alt="${item.name}" class="img-fluid">`}
                          </div>
                          <div class="col-5">
                            <strong>${item.name}</strong><br>
                            Giá: ${item.price} VND
                          </div>
                          <div class="col-2">
                            x ${item.quantity}
                          </div>
                          <div class="col-2 text-end">
                            ${item.item_total} VND
                          </div>
                        </div>
                        <button class="btn btn-danger btn-sm remove-from-cart" data-product="${item.product_id}">&times;</button>
                      </li>`;
                    });
                    html += '</ul>';
                    html += `<div class="mt-3"><h5>Tạm tính: ${data.order_total} VND</h5></div>`;
                    contentDiv.innerHTML = html;
                } else {
                    contentDiv.innerHTML = "<p>Giỏ hàng của bạn đang trống.</p>";
                }
            })
            .catch(error => {
                console.error("Lỗi tải giỏ hàng:", error);
                document.getElementById("mini-cart-content").innerHTML = "<p>Có lỗi xảy ra khi tải giỏ hàng.</p>";
            });
    }



    // Khi offcanvas mini-cart mở ra, cập nhật dữ liệu giỏ hàng
    let miniCartOffcanvas = document.getElementById("miniCartOffcanvas");
    miniCartOffcanvas.addEventListener("shown.bs.offcanvas", function () {
        updateMiniCart();
    });

    function updateCartCount(count) {
        let cartCountElement = document.getElementById("cart-count");
        if (cartCountElement) {
            cartCountElement.textContent = count;
        }
    }

    function showMessage(message, type) {
        var cartMessage = document.getElementById("cart-message");
        if (cartMessage) {
            cartMessage.textContent = message;
            cartMessage.className = "alert alert-" + type;
            cartMessage.classList.remove("d-none");
            setTimeout(function () {
                cartMessage.classList.add("d-none");
            }, 2000);
        } else {
            alert(message);
        }
    }


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

    document.getElementById('contact-toggle').addEventListener('click', function () {
        var icons = document.querySelector('.contact-icons');
        icons.classList.toggle('hidden');
    });

});

