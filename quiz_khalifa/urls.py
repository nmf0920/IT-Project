"""
URL configuration for quiz_khalifa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from friends import views as friend_views
from message import views as message_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", user_views.register, name="user-register"),
    path("login/", auth_views.LoginView.as_view(template_name = "user-templates/login.html"), name="user-login"),
    path("logout/", auth_views.LogoutView.as_view(), name="user-logout"),
    path("addfriend/", friend_views.addfriends, name="add-friend"),
    path("messageWindow/", message_views.messageWindow, name="message-window"),
    path("", include('quizkhalifa.urls')),  
]
