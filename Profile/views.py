from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def profile(request):
    return render(request, 'Profile/profile.html')

def registerpage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for '+ user)

                return redirect('login')

        return render(request, 'Profile/registerpage.html', {'form':form})

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            
            else:
                messages.info(request, 'username or password is incorrect')
                return render(request, 'Profile/login.html')
        return render(request, 'Profile/login.html')


def logoutuser(request):
    logout(request)
    return redirect('login')