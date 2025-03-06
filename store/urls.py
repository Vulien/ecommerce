from django.urls import path
from . import views 
from .views import home, log, qa, product_list, product_detail,  cart_view, add_to_cart, remove_from_cart, checkout, login_page, cart_count, get_cart, about, contact, policy, check, delivery, shopping, security  # Import views
from django.contrib.auth import views as auth_views

#from chat.views import chat_view

urlpatterns = [
    #path('', home, name='home'),  # Trang chủ
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path('san-pham/', product_list, name='products'),  # Sản phẩm
    path('dang-nhap/', login_page, name='login'),  # Đăng nhập
    path('checkout/', views.checkout, name='checkout'),
    path('gio-hang/', views.cart_view, name='cart_view'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart-count/', views.cart_count, name='cart_count'),
    path("get-cart/", views.get_cart, name="get_cart"),
    path('contact/', views.contact, name='contact'),
    path('policy/', policy, name='policy'),
    path('check/', check, name='check'),
    path('delivery/', delivery, name='delivery'),
    path('shopping/', shopping, name='shopping'),
    path('security/', security, name='security'),
    path("product_detail/<int:product_id>/", views.product_detail, name="product_detail"),
    path('mk/', views.log, name='log'),
    path('qa/', views.qa, name='qa'),
 
] 


