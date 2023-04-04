from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def landingPage(request):
    return render(request, 'bridge/landingPage.html')


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'bridge/loginPage.html', {'error': 'Invalid username or password'})

    return render(request, 'bridge/loginPage.html')


def logoutUser(request):
    logout(request)
    return redirect('landingPage')


@login_required(login_url='loginPage')
def home(request):
    return render(request, 'bridge/home.html')
