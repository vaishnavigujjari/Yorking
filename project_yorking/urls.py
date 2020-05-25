from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('',include('Home.urls')),
    path('/createteam',include('CreateTeam.urls')),
    path('/leaderboard',include('LeaderBoard.urls')),
    path('/playerdashboard',include('PlayerDashboard.urls')),
    path('/profile',include('Profile.urls')),
    path('admin/', admin.site.urls),
]
