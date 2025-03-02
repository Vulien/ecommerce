"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
#from chat import views
#from chat.views import home_with_chat


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),  # Kết nối với urls.py của store
   # path("admin-chat/", views.admin_chat, name="admin_chat"),
  #  path("chat/", include("chat.urls")),
    path("accounts/", include("accounts.urls")),
  #  path("", home_with_chat, name="home"),
  #  re_path(r"^", include("chat.urls")),
  path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico', permanent=True)),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
