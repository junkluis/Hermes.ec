

import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from Heraldo.models import Rol, Driver, DriverStatus
from django.core.exceptions import ObjectDoesNotExist



def index(request):
    return redirect('dashboard')

def login_zeus(request):
    if request.method =='POST':
        try:
            email = request.POST["email"]
            password = request.POST["password"]
            username = User.objects.get(email=email).username
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'Zeus/login.html', {})
        except:
            return render(request, 'Zeus/login.html', {})
    else:
        return render(request, 'Zeus/login.html', {})
    
@login_required(login_url="/login")
def dashboard(request):
    return render(request, 'Zeus/index.html', {})

@login_required(login_url="/login")
def users(request):
    context = {}
    user_list = User.objects.filter(is_active=True)
    user_list_json = []
    for user in user_list:
        try:
            user_rol = Rol.objects.get(user=user)
            user.user_rol = user_rol.user_rol
        except ObjectDoesNotExist:
            user.user_rol = None

        user_list_json.append({
            'id': user.id,
            'name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'user_rol': user.user_rol,
        })
    context['user_list'] = user_list_json
    return render(request, 'Zeus/user-list.html', context)

@login_required(login_url="/login")
def new_user(request):
    if request.method =='POST':
        name = request.POST["name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        rol = request.POST["rol"]
        new_user = User.objects.create(
            username=str(name+last_name),
            first_name=name,
            last_name=last_name,
            email=email
        )
        new_user.set_password(password)
        new_user.save()
        Rol.objects.create(
            user=new_user,
            user_rol=rol
        )
        return redirect('users')
    else:
        context = {}
        return render(request, 'Zeus/new-user.html', context)

def not_implemented(request):
    return render(request, 'Zeus/working.html', {})

def logout_zeus(request):
    logout(request)
    return redirect('login')