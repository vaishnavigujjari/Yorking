from django.contrib import admin
from django.urls import path,include
from . import views
from CreateTeam.views import players,user_team,select_match,dashboard


urlpatterns = [
    path('', views.select_match, name='select_match'),
    path('chooseplayers',views.players, name='players'),
    path('user_team',views.user_team, name='user_team'),
    path('dashboard',views.dashboard, name='dashboard'),
]