from django.shortcuts import render

# Create your views here.
def select_match(request):
    return render(request, 'createteam/select_match.html')