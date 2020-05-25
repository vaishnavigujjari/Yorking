from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.select_match, name='select_match')
]