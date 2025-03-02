from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from accounts.models import CustomUser
from django.contrib import messages


def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Đăng nhập thành công!")
            return redirect("home")  # Thay "home" bằng tên URL của trang chủ
        else:
            messages.error(request, "Email hoặc mật khẩu không đúng!")
    
    return render(request, "accounts/login.html")

def user_logout(request):
    logout(request)
    return redirect("home")

def login_email(request):
    if request.method == "POST":
        email = request.POST["email"]
        request.session["email"] = email
        return redirect("chat_home")
    return render(request, "accounts/login.html")

