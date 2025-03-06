

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Order, OrderItem, Category
from .forms import ReviewForm
import random
import string


def home(request):
    products = Product.objects.all()
    bestselling_products = Product.objects.all()[:4]
    return render(request, 'store/index.html', {'products': products,
                                                'bestselling_products': bestselling_products,
                                                })

def about(request):
    return render(request, "store/about.html")

def product_list(request):
   
    category_slug = request.GET.get('category')
    categories = Category.objects.all()
    sort = request.GET.get('sort')
    if category_slug:
        products = Product.objects.filter(category__slug=category_slug)
    else:
        products = Product.objects.all()
        
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')
    # nếu sort="" hoặc None -> giữ mặc định
    context = {
        'categories': categories,
        'products': products,
        'selected_category': category_slug,
        'sort': sort,
    }
    return render(request, 'store/home.html', context)  # Truyền dữ liệu vào template

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    extra_images = product.images.all()
    reviews = product.reviews.order_by('-created_at')
    similar_products = Product.objects.exclude(id=product.id)[:4]

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, 'store/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
        'similar_products': similar_products,
        'extra_images': extra_images,
    })

def login_page(request):
    return render(request, 'store/login.html')


def contact(request):
    return render(request, "store/contact.html")


def generate_order_code():
    
    return "HUST - " + ''.join(random.choices(string.digits, k=6)) 

def cart_view(request):
    """
    Hiển thị trang giỏ hàng và form thanh toán.
    """
    cart = request.session.get("cart", {})
    cart_items = []
    total_price = 0
    order_code = generate_order_code()
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * quantity
        total_price += item_total
        cart_items.append({
            "product": product,
            "quantity": quantity,
            "item_total": item_total
        })
    context = {
        "cart_items": cart_items,
        "total_price": total_price,
        "order_code": order_code
    }
    return render(request, "store/cart.html", context)

@csrf_exempt  # Bỏ kiểm tra CSRF (chỉ dùng nếu không muốn xử lý CSRF)
def add_to_cart(request):
    if request.method == "POST":
        import json
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        product_id = str(data.get("product_id"))
        # Lấy số lượng, mặc định là 1 nếu không có
        try:
            quantity = int(data.get("quantity", 1))
        except (ValueError, TypeError):
            quantity = 1
        cart = request.session.get("cart", {})
        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity
        request.session["cart"] = cart
        cart_count = sum(cart.values())
        return JsonResponse({"cart_count": cart_count})
    return JsonResponse({"error": "Invalid request"}, status=400)

def add_one_to_cart(request, product_id):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        pid_str = str(product_id)
        if pid_str in cart:
            cart[pid_str] += 1
        else:
            cart[pid_str] = 1
        request.session["cart"] = cart
        return JsonResponse({"success": True, "cart_count": sum(cart.values())})
    return JsonResponse({"error": "Invalid request"}, status=400)

def get_cart(request):
   
    cart = request.session.get("cart", {})
    cart_items = []
    order_total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * quantity
        order_total += item_total
        cart_items.append({
            "product_id": product.id,
            "name": product.name,
            "quantity": quantity,
            "price": str(product.price),
            "item_total": str(item_total),
            "image_url": product.image.url if product.image else ""
        })
    return JsonResponse({"cart_items": cart_items, "order_total": str(order_total)})

@csrf_exempt  # Bỏ kiểm tra CSRF (chỉ dùng nếu không muốn xử lý CSRF)
def remove_from_cart(request, product_id):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        product_id = str(product_id)

        if product_id in cart:
            del cart[product_id]
            request.session["cart"] = cart

            # Tính lại tổng tiền
            total_price = 0
            for pid, qty in cart.items():
                product = Product.objects.get(id=pid)
                total_price += product.price * qty

            return JsonResponse({
                "success": True,
                "cart_count": sum(cart.values()),
                "total_price": total_price,
            })
        else:
            return JsonResponse({"success": False, "error": "Sản phẩm không tồn tại"})

    return JsonResponse({"error": "Yêu cầu không hợp lệ"}, status=400)



def cart_count(request):
    cart = request.session.get("cart", {})
    count = sum(cart.values())
    return {'cart_count': count}


def checkout(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        email = request.POST.get("email", "").strip() 
        payment_method = request.POST.get("payment_method", "").strip()
        country = request.POST.get("country")
        city = request.POST.get("city")
        
        if city.strip().lower() == "hà nội":
            shipping_fee = 0
        else:
            shipping_fee = 30000
            
       

        # Kiểm tra các trường bắt buộc
        if not name or not phone or not address or not email or not payment_method:
            messages.error(request, "Vui lòng điền đầy đủ các trường bắt buộc!")
            return redirect("cart_view")

        cart = request.session.get("cart", {})
        if not cart:
            messages.error(request, "Giỏ hàng của bạn đang trống!")
            return redirect("cart_view")

        # Tạo đơn hàng
        order = Order.objects.create(
            name=name,
            phone=phone,
            address=address,
            email=email if email else None,
            payment_method=payment_method
        )

        # Tạo các OrderItem cho từng sản phẩm trong giỏ
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product.name,
                quantity=quantity,
                price=product.price
            )

        # Xóa giỏ hàng sau khi đặt hàng thành công
        request.session["cart"] = {}

        # Thông báo đặt hàng thành công
        if payment_method == "qr":
            messages.success(
                request,
                "🎉 Đặt hàng thành công! Vui lòng gửi ảnh xác nhận qua Messenger (Facebook: <a href='https://www.facebook.com/profile.php?id=61573514560235&mibextid=wwXIfr&rdid=3TRYWe0PDCPEI5qn&share_url=https%3A%2F%2Fwww.facebook.com%2Fshare%2F1BH1T37MyC%2F%3Fmibextid%3DwwXIfr' target='_blank'>Nhấn vào đây</a>). Trạng thái đơn hàng của bạn sẽ được gửi qua email"
            )
        else:
            messages.success(request, "🎉 Đặt hàng thành công! Bạn sẽ thanh toán khi nhận hàng. Trạng thái đơn hàng của bạn sẽ được gửi qua email")
        return redirect("cart_view")

    return redirect("cart_view")



def order_list(request):
    orders = Order.objects.prefetch_related("items").order_by("-created_at")
    return render(request, "store/order_list.html", {"orders": orders})

def policy(request):
    return render(request, "store/policy.html")

def check(request):
    return render(request, "store/check.html")

def delivery(request):
    return render(request, "store/delivery.html")

def shopping(request):
    return render(request, "store/shopping.html")

def security(request):
    return render(request, "store/security.html")

def log(request):
    return render(request, "store/log.html")

def qa(request):
    return render(request, "store/QA.html")