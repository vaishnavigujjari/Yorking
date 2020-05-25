from django.shortcuts import render

# Create your views here.
def selectmatch(request):
    return render(request,'playerdashboard/selectmatch.html')