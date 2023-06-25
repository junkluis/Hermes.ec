import csv
import re
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from Heraldo.models import Rol, Driver, DriverStatus, Truck, Order
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict


from Zeus.constants import CAR_YEARS_CHOICES, ORDER_STATUS, MAP_KEY


def index(request):
    return redirect('dashboard')

def dashboard_v2(request):
    context = {}
    return render(request, 'Zeus/base-v2.html', context)

def login_zeus(request):
    context = {}
    if request.method =='POST':
        try:
            email = request.POST["email"]
            password = request.POST["password"]
            user = User.objects.get(email=email)
            try:
                rol = Rol.objects.get(user=user)
            except:
                context['error'] = True
                context['error_message'] = "El usuario no tiene permisos suficientes"
                return render(request, 'Zeus/v2/login.html', context)
                
            if rol.user_rol != 'AD':
                context['error'] = True
                context['error_message'] = "El usuario no tiene permisos suficientes"
                return render(request, 'Zeus/v2/login.html', context)

            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                context['error'] = True
                context['error_message'] = "El usuario o contraseña son inválidos"
                return render(request, 'Zeus/v2/login.html', context)
        except:
            context['error'] = True
            context['error_message'] = "El usuario o contraseña son inválidos"
            return render(request, 'Zeus/v2/login.html', context)
    else:
        return render(request, 'Zeus/v2/login.html', context)
    
@login_required(login_url="/login")
def dashboard(request):
    context = {}
    context['gkey'] = MAP_KEY

    # Obtener Ordenes
    ordenes = Order.objects.filter(status='EP')
    ordenes_json = []
    for orden in ordenes:
        orden_json = {}
        orden_json['camion'] = orden.truck.license
        orden_json['ruta'] = orden.origin + ' - ' + orden.destination
        orden_json['location'] = (orden.location_coord_lat, orden.location_coord_long)
        orden_json['destination'] = (orden.destination_coord_lat, orden.destination_coord_long)
        orden_json['status'] = orden.status
        ordenes_json.append(orden_json)

    context['ordenes'] = ordenes_json
    return render(request, 'Zeus/v2/index.html', context)

@login_required(login_url="/login")
def users(request):
    context = {}
    user_list = User.objects.all()
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
            'is_active': user.is_active,
        })
    context['user_list'] = user_list_json
    return render(request, 'Zeus/v2/user-list.html', context)

@login_required(login_url="/login")
def new_user(request):
    if request.method =='POST':
        context = {}

        identification = request.POST["identification"]
        name = request.POST["name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        rol = request.POST["rol"]

        error_list = []
        user_exist = User.objects.filter(username=identification)
        if len(user_exist) > 0:
            error_list.append('La Identificación ya fue usada')
        
        password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$"
        if re.match(password_pattern, password) is None:
            error_list.append('La contraseña debe contener al menos 8 caracteres, una minúscula, una mayúscula y un número')
        
        if len(error_list) > 0:
            context['error'] = True
            context['error_list'] = error_list
            context['confirm_user'] = {
                'username': identification,
                'first_name': name,
                'last_name': last_name,
                'last_name': email,
            }
            context['action'] = 'edit'
            return render(request, 'Zeus/v2/new-user.html', context)

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
        return render(request, 'Zeus/v2/new-user.html', context)

@login_required(login_url="/login")
def trucks(request):
    context = {}
    truck_list = Truck.objects.all()
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
            'license': truck.license,
            'is_active': truck.is_active
        })
    context['truck_list'] = truck_list_json
    return render(request, 'Zeus/v2/truck-list.html', context)

@login_required(login_url="/login")
def orders(request):
    context = {}
    order_list = Order.objects.all()
    order_list_json = []
    for order in order_list:
        order_json = model_to_dict(order)
        order_json['client'] = order.client.first_name + ' ' + order.client.last_name
        order_json['admin'] = order.responsible.first_name + ' ' + order.responsible.last_name
        order_json['driver'] = order.driver.first_name + ' ' + order.driver.last_name
        order_json['truck'] = order.truck.brand + ' - ' + order.truck.license
        order_json['status'] = ORDER_STATUS[order.status]
        order_list_json.append(order_json)
    
    context['order_list'] = order_list_json
    return render(request, 'Zeus/v2/order-list.html', context)

@login_required(login_url="/login")
def view_orders(request, order_id):
    context = {}
    #try:
    order_info = Order.objects.filter(id=order_id).first()
    context['order'] = order_info
    context['gkey'] = MAP_KEY
    
    current_lat = float(order_info.location_coord_lat)
    current_long = float(order_info.location_coord_long)
    context['current_location'] = (current_lat, current_long)

    destination_lat = float(order_info.destination_coord_lat)
    destination_long = float(order_info.destination_coord_long)
    context['destination_location'] = (destination_lat, destination_long)
    return render(request, 'Zeus/v2/order-view.html', context)
    # except:
      #  return redirect('dashboard')



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
        return render(request, 'Zeus/v2/new-truck.html', context)

@login_required(login_url="/login")
def delete(request, object, key_id):
    if request.method =='POST':
        if request.POST["object"] == 'user':
            user_id = request.POST["id"]
            user = User.objects.get(id=user_id)
            user.is_active = False
            user.save()
            return redirect('users')

        elif request.POST["object"] == 'truck':
            truck_id = request.POST["id"]
            truck = Truck.objects.get(id=truck_id)
            truck.is_active = False
            truck.save()
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
        return render(request, 'Zeus/v2/are-you-sure.html', context)

@login_required(login_url="/login")
def reactivate(request, object, key_id):
    if object == 'user':
        user = User.objects.get(pk=key_id)
        user.is_active = True
        user.save()
        return redirect('users')

    elif object == 'truck':
        truck = Truck.objects.get(pk=key_id)
        truck.is_active = True
        truck.save()
        return redirect('trucks')
    
@login_required(login_url="/login")
def edit(request, object, key_id):
    if request.method =='POST':
        if request.POST["object"] == 'user':
            context = {}
            user_id = request.POST["user_id"]
            user = User.objects.get(id=user_id)

            identification = request.POST["identification"]
            name = request.POST["name"]
            last_name = request.POST["last_name"]
            email = request.POST["email"]
            password = request.POST["password"]
            rol = request.POST["rol"]

            error_list = []
            password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$"
            if re.match(password_pattern, password) is None:
                error_list.append('La contraseña debe contener al menos 8 caracteres, una minúscula, una mayúscula y un número')
            
            if len(error_list) > 0:
                context['error'] = True
                context['error_list'] = error_list
                context['confirm_user'] = {
                    'username': identification,
                    'first_name': name,
                    'last_name': last_name,
                    'last_name': email,
                }
                context['action'] = 'edit'
                return render(request, 'Zeus/v2/new-user.html', context)

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
            return render(request, 'Zeus/v2/new-user.html', context)

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

            return render(request, 'Zeus/v2/new-truck.html', context)

def not_implemented(request):
    return render(request, 'Zeus/v2/working.html', {})

def logout_zeus(request):
    logout(request)
    return redirect('login')

def donwload_users(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="csv/users.csv"'},
    )
    
    user_list = User.objects.all().order_by('-is_active').values()
    
    writer = csv.writer(response)
    writer.writerow(user_list[0].keys())
    for user in user_list:
        writer.writerow(user.values())

    return response

def donwload_truck(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="csv/trucks.csv"'},
    )
    
    truck_list = Truck.objects.all().order_by('-is_active').values()
    
    writer = csv.writer(response)
    writer.writerow(truck_list[0].keys())
    for truck in truck_list:
        writer.writerow(truck.values())

    return response