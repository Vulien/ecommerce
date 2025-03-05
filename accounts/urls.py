
from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import user_login, user_logout, user_register

urlpatterns = [
    path('login/', user_login, name='login'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path("logout/", user_logout, name="logout"),
    path("register/", user_register, name="register"),
]
