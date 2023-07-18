"""
URL configuration for SocialApi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from socialsite.views import (FriendRequestAPIView, UserCreateAPIView,
                              UserLoginAPIView, UserSearchAPIView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', UserCreateAPIView.as_view(), name='user-create'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('search/', UserSearchAPIView.as_view(), name='user-search'),
    path('friend-requests/', FriendRequestAPIView.as_view(), name='friend-request'),
    path('friend-requests/<int:pk>/', FriendRequestAPIView.as_view(), name='friend-request-action'),
]
