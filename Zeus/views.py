

import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from Heraldo.models import Rol, Driver, DriverStatus, Truck
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict


from Zeus.constants import CAR_YEARS_CHOICES


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
            'username': user.username,
        })
    context['user_list'] = user_list_json
    return render(request, 'Zeus/user-list.html', context)

@login_required(login_url="/login")
def new_user(request):
    if request.method =='POST':
        identification = request.POST["identification"]
        name = request.POST["name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        rol = request.POST["rol"]

        new_user = User.objects.create(
            username=identification,
            first_name=name,
            last_name=last_name,
            email=email
        )
        new_user.set_password(password)
        new_user.save()

        if rol is not 'None':
            Rol.objects.create(
                user=new_user,
                user_rol=rol
            )
        return redirect('users')
    else:
        context = {
            'action': 'new'
        }
        return render(request, 'Zeus/new-user.html', context)

@login_required(login_url="/login")
def trucks(request):
    context = {}
    truck_list = Truck.objects.filter(is_active=True)
    truck_list_json = []
    for truck in truck_list:
        driver = truck.user
        driver_name = ''
        if driver:
            driver_name = driver.first_name + ' ' + driver.last_name
            
        truck_list_json.append({
            'id': truck.id,
            'driver': driver_name,
            'capacity': str(truck.capacity) + ' ' +truck.measurement, 
            'brand': truck.brand,
            'color': truck.color,
        })
    context['truck_list'] = truck_list_json
    return render(request, 'Zeus/truck-list.html', context)


@login_required(login_url="/login")
def new_truck(request):
    if request.method =='POST':
        driver_id = request.POST["driver"]

        
        try:
            driver = User.objects.get(pk=driver_id)
        except Rol.DoesNotExist:
            driver = None
        Truck.objects.create(
            user = driver,
            license = request.POST["license"],
            capacity = request.POST["capacity"],
            measurement = request.POST["unit"],
            color = request.POST["color"],
            brand = request.POST["brand"],
            year = request.POST["year"],
        )

        return redirect('trucks')
    else:
        context = {}
        user_list = User.objects.filter(is_active=True)
        driver_list_json = []
        for user in user_list:
            try:
                rol = Rol.objects.get(user=user)
            except Rol.DoesNotExist:
                rol = None

            if rol and rol.user_rol == 'DR':
                driver_list_json.append({
                    'id': user.id,
                    'name': user.first_name,
                    'last_name': user.last_name,
                })
        
        context['driver_list_json'] = driver_list_json
        context['car_years_choices'] = CAR_YEARS_CHOICES
        return render(request, 'Zeus/new-truck.html', context)

@login_required(login_url="/login")
def delete(request, object, key_id):
    if request.method =='POST':
        if request.POST["object"] == 'user':
            user_id = request.POST["id"]
            User.objects.get(id=user_id).delete()
            return redirect('users')

        elif request.POST["object"] == 'truck':
            truck_id = request.POST["id"]
            Truck.objects.get(id=truck_id).delete()
            return redirect('trucks')

    else:
        context = {}
        if object == 'user':
            user = User.objects.get(pk=key_id)
            user_json = model_to_dict(user)
            context['confirm_user'] = user_json

        elif object == 'truck':
            truck = Truck.objects.get(pk=key_id)
            truck_json = model_to_dict(truck)
            context['confirm_truck'] = truck_json
        return render(request, 'Zeus/are-you-sure.html', context)
    
@login_required(login_url="/login")
def edit(request, object, key_id):
    if request.method =='POST':
        if request.POST["object"] == 'user':
            
            user_id = request.POST["user_id"]
            user = User.objects.get(id=user_id)

            identification = request.POST["identification"]
            name = request.POST["name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            password = request.POST["password"]
            rol = request.POST["rol"]

            user.username = identification
            user.first_name = name
            user.last_name = last_name
            user.email = email

            user.set_password(password)
            user.save()

            current_rol = Rol.objects.get(user=user)
            current_rol.user_rol = rol
            current_rol.save()

            return redirect('users')

        if request.POST["object"] == 'truck':

            truck_id = request.POST["truck_id"]
            truck = Truck.objects.get(id=truck_id)
            try:
                driver = User.objects.get(pk=truck.user.id)
            except Rol.DoesNotExist:
                driver = None

            truck.user = driver
            truck.license = request.POST["license"]
            truck.capacity = request.POST["capacity"]
            truck.measurement = request.POST["unit"]
            truck.color = request.POST["color"]
            truck.brand = request.POST["brand"]
            truck.year = request.POST["year"]
            truck.save()
            
            return redirect('trucks')
    else:
        context = {}
        context['action'] = 'edit'
        if object == 'user':
            user = User.objects.get(id=key_id)
            user_json = model_to_dict(user)
            context['confirm_user'] = user_json
            return render(request, 'Zeus/new-user.html', context)

        if object == 'truck':
            user_list = User.objects.filter(is_active=True)
            driver_list_json = []
            for user in user_list:
                try:
                    rol = Rol.objects.get(user=user)
                except Rol.DoesNotExist:
                    rol = None

                if rol and rol.user_rol == 'DR':
                    driver_list_json.append({
                        'id': user.id,
                        'name': user.first_name,
                        'last_name': user.last_name,
                    })
            
            context['driver_list_json'] = driver_list_json
            context['car_years_choices'] = CAR_YEARS_CHOICES

            truck = Truck.objects.get(id=key_id)
            truck_json = model_to_dict(truck)
            context['confirm_truck'] = truck_json

            return render(request, 'Zeus/new-truck.html', context)

def not_implemented(request):
    return render(request, 'Zeus/working.html', {})

def logout_zeus(request):
    logout(request)
    return redirect('login')