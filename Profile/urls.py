from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.profile,name='profile'),
    path('register', views.registerpage,name='register'),
    path('login', views.loginpage, name='login'),
    path('logout', views.logoutuser, name='logout')
]