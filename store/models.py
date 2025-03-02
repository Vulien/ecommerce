from django.db import models
import random
import string
#from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)  # Tên sản phẩm
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Giá sản phẩm
    description = models.TextField(blank=True, null=True)  # Mô tả sản phẩm
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # Ảnh sản phẩm

    def __str__(self):
        return self.name  # Hiển thị tên sản phẩm trong admin


class Order(models.Model):
    PAYMENT_CHOICES = [
        ("qr", "Thanh toán online qua QR"),
        ("cod", "Thanh toán khi nhận hàng (COD)"),
    ]
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    email = models.EmailField(default="default@example.com")  
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    processed = models.BooleanField(default=False, verbose_name="Đã lên đơn")
    created_at = models.DateTimeField(auto_now_add=True)
    order_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.order_code:
            self.order_code = self.generate_order_code()
        super().save(*args, **kwargs)

    def generate_order_code(self):
        return "HUST-" + ''.join(random.choices(string.digits, k=6))

    def __str__(self):
        return f"Order {self.id} - {self.name} ({self.get_payment_method_display()})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.CharField(max_length=255)  # lưu tên sản phẩm
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product} (Order {self.order.id})"
    

class Review(models.Model):
    RATING_CHOICES = [(1, "⭐"), (2, "⭐⭐"), (3, "⭐⭐⭐"), (4, "⭐⭐⭐⭐"), (5, "⭐⭐⭐⭐⭐"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.name}"