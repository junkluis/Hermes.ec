from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def index(request):
    return HttpResponse("Habla para que yo te conozca.")

def login_zeus(request):
    if request.method =='POST':
        email = request.POST["email"]
        password = request.POST["password"]
        username = User.objects.get(email=email).username
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'Zeus/login.html', {})
    else:
        return render(request, 'Zeus/login.html', {})
    
@login_required(login_url="/login")
def dashboard(request):
    return render(request, 'Zeus/index.html', {})
