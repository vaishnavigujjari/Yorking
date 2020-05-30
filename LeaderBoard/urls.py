from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.Leaderboard,name='Leaderboard'),
    path('leaderboardeval', views.leaderboardeval, name='leaderboardeval'),
    path('get_points', views.get_points, name='get_points'),
    path('update_scores', views.update_scores, name='update_scores'),
    # path('matchlist',views.matchlist,name='matchlist')
]