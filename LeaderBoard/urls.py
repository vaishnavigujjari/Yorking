from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.choosematch,name='choosematch'),
    path('matchlist',views.matchlist,name='matchlist')
]