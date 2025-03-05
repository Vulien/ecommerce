from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from accounts.models import CustomUser
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm

def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            if not request.POST.get('remember_me'):
                request.session.set_expiry(0)
            messages.success(request, "Đăng nhập thành công!")
            return render(request, "store/index.html") # Thay "home" bằng tên URL của trang chủ
        else:
            messages.error(request, "Email hoặc mật khẩu không đúng!")
    
    return render(request, "accounts/login.html")


def user_logout(request):
    logout(request)
    return redirect("home")

def user_register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Đăng ký thành công! Vui lòng đăng nhập.")
            return redirect("login")
        else:
            messages.error(request, "Có lỗi xảy ra. Vui lòng kiểm tra lại thông tin.")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

