from django.shortcuts import render
from CreateTeam.models import country_team, match_user, user_team, choosen_players, match_performance
from django.http import JsonResponse 
from django.views.generic import View

def choosematch(request):
    return render(request, 'leaderboard/choosematch.html', name='choosematch')