from django.shortcuts import render

# Create your views here.
def choosematch(request):
    return render(request,'leaderboard/choosematch.html')