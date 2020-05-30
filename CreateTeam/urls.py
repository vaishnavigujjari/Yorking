from django.contrib import admin
from django.urls import path,include
from . import views
from CreateTeam.views import players,userteam,select_match,congrats


urlpatterns = [
    path('', views.select_match, name='select_match'),
    path('chooseplayers',views.players, name='players'),
    path('userteam',views.userteam, name='userteam'),
    path('congrats',views.congrats, name='congrats'),
    path('get_points',views.get_points,name="get_points"),
    path('update_scores',views.update_scores,name='update_scores'),
    path('constraints',views.constraints,name='constraints'),
]