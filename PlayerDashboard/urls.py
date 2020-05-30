from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.selectmatch,name='selectmatch'),
    path('matches', views.matches, name='matches'),
    path('pdm1',views.pdm1, name='pdm1'),
]