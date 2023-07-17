import csv
import re
import json
import pdfkit

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from Heraldo.models import Rol, Driver, DriverStatus, Truck, Order, Ubicacion, Tarifas, OrdersFile, Console, changePasswordToken, Formulario
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
import datetime
import hashlib

from django.core.mail import EmailMessage


from Zeus.constants import CAR_YEARS_CHOICES, ORDER_STATUS, MAP_KEY, USER_MAIL,  USER_MAIL_PASSWORD, SITE_URL


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
        orden_json['id'] = orden.id
        ordenes_json.append(orden_json)

    context['ordenes'] = ordenes_json
    return render(request, 'Zeus/v2/index.html', context)

@login_required(login_url="/login")
def users(request):
    context = {}
    user_list = User.objects.filter().order_by('date_joined')
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
            'date_joined': user.date_joined,
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

        if password != None and password != '':
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
                'email': email,
            }
            context['action'] = 'edit'
            return render(request, 'Zeus/v2/new-user.html', context)

        new_user = User.objects.create(
            username=identification,
            first_name=name,
            last_name=last_name,
            email=email
        )

        if password is not None:
            new_user.set_password(password)
            new_user.save()

        if rol != 'None':
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
    truck_list = Truck.objects.filter().order_by('creation_date')
    truck_list_json = []
    for truck in truck_list:
        driver = truck.user
        driver_name = ''
        if driver:
            driver_name = driver.first_name + ' ' + driver.last_name
            
        truck_list_json.append({
            'id': truck.id,
            'driver': driver_name,
            'capacity': f'{truck.capacity:.2f}' + ' ' +truck.measurement, 
            'brand': truck.brand,
            'color': truck.color,
            'color_name': truck.color_name,
            'status': truck.status,
            'license': truck.license,
            'is_active': truck.is_active
        })
    context['truck_list'] = truck_list_json
    return render(request, 'Zeus/v2/truck-list.html', context)

@login_required(login_url="/login")
def orders(request):
    context = {}
    order_list = Order.objects.filter(status__in=['EP', 'PD']).order_by('creation_date').reverse()
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
    context['view_title'] = 'Ordenes En Proceso o Pendientes'
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
        except:
            driver = None

        Truck.objects.create(
            user = driver,
            license = request.POST["license"],
            capacity = request.POST["capacity"],
            measurement = request.POST["unit"],
            color = request.POST["color"],
            color_name = request.POST["colorName"],
            status = request.POST["estado"],
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
def new_order(request):
    if request.method =='POST':
        context = {}



        '''
        'client': ['26'],
         'driver': ['13'],
         'contenido': ['asdasdasdas'], 
         'pesoValue': ['2'], 
         'unitSelect': ['To'], 
         'tarifaAplicada': ['8.50'], 
         'originPoint': ['-2.28000000;-79.91000000;Puerto Marítimo de Guayaquil'], 
         'destinoPoint': ['-2.18982293;-79.88768578;Parque Centenario'], 
         'distanciaInput': ['11.81 Km'], 
         'precioInput': ['100.39'
        '''


        client_id = request.POST['client']
        driver_id = request.POST['driver']
        contenido = request.POST['contenido']
        origen = request.POST['originPoint'].split(';')
        destino = request.POST['destinoPoint'].split(';')
        precio = float(request.POST['precioInput'])
        peso = float(request.POST['pesoValue'])
        unit = request.POST['unitSelect']
        tarifa = float(request.POST['tarifaAplicada'])
        distancia = float(request.POST['distanciaInput'].split(' ')[0])
        placa = request.POST['camionAsignado']
        

        responsible = User.objects.get(username = request.user.username)
        client = User.objects.get(id=client_id)
        driver = User.objects.get(id=driver_id)
        camion = Truck.objects.filter(license=placa).first()

        new_order = Order.objects.create(
            responsible=responsible,
            driver=driver,
            client=client,
            truck=camion,
            content=contenido,
            origin=origen[2],
            origin_coord_lat=origen[0],
            origin_coord_long=origen[1],
            destination=destino[2],
            destination_coord_lat=destino[0],
            destination_coord_long=destino[1],
            location_coord_lat=origen[0],
            location_coord_long=origen[1],
            peso=peso,
            tarifa=tarifa,
            precio= precio,
            distancia= distancia,
            unidad=unit,
        )
        
        guia_remision = request.FILES['guiaRemision']
        archivos_legales = request.FILES.getlist('archivosLegales')

        guia_remision_file = Console.objects.create(
            name= guia_remision.field_name,
            archivo= guia_remision,
        )

        OrdersFile.objects.create(
            orden=new_order,
            archivo=guia_remision_file,
            nombre='Guia de Remision para orden - ' + str(new_order.id)
        )

        for archivo in archivos_legales:
            archivo_raw = Console.objects.create(
                name= archivo._name,
                archivo=archivo,
            )
            OrdersFile.objects.create(
                orden=new_order,
                archivo=archivo_raw,
                nombre=archivo._name
            )

        return redirect('orders')


    else:
        user_list = User.objects.filter()
        
        client_list = []
        driver_list = []
        
        inactive_driver = []
        busy_driver = []
        inactive_truck = []


        for user in user_list:
            try:
                rol = Rol.objects.get(user=user)
            except Rol.DoesNotExist:
                rol = None

            if rol and rol.user_rol == 'DR':
                driver_json = {
                    'id': user.id,
                    'name': user.first_name,
                    'last_name': user.last_name,
                    'identificacion': user.username
                }
                truck = Truck.objects.filter(user=user).first()
                orders = Order.objects.filter(driver=user, status='EP').first()

                if truck:
                    driver_json['placa'] = truck.license
                else:
                    driver_json['placa'] = 'Sin asignar'

                if not user.is_active:
                    inactive_driver.append(driver_json)
                elif driver_json['placa'] == 'Sin asignar':
                    inactive_truck.append(driver_json)
                elif truck.status != 'Disponible':
                    inactive_truck.append(driver_json)
                elif orders is not None:
                    busy_driver.append(driver_json)
                else:
                    driver_list.append(driver_json)
                
            
            if rol and rol.user_rol == 'CL':
                if user.is_active:
                    client_json = {
                        'id': user.id,
                        'name': user.first_name,
                        'last_name': user.last_name,
                        'identificacion': user.username
                    }
                    client_list.append(client_json)

                
        tarifas = Tarifas.objects.all().first()
        ubicaciones = Ubicacion.objects.all()
        ubicaciones_json = []

        for ubicacion in ubicaciones:
            ubicaciones_json.append(model_to_dict(ubicacion))


        context = {
            'action': 'new'
        }
        context['gkey'] = MAP_KEY
        context['client_list'] = client_list
        context['driver_list'] = driver_list
        context['inactive_driver'] = inactive_driver
        context['busy_driver'] = busy_driver
        context['inactive_truck'] = inactive_truck
        context['tarifas'] = model_to_dict(tarifas)
        context['ubicaciones'] = ubicaciones_json

        return render(request, 'Zeus/v2/new-order.html', context)


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
            if password != None and password != '':
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
                    'email': email,
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

@login_required(login_url="/login")
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

@login_required(login_url="/login")
def hermes_settings(request):
    context = {}

    if request.method =='POST':
        if request.POST["action"] == 'add_location':
            new_location = Ubicacion.objects.create(
                nombre=request.POST['nombre'],
                latitud=float(request.POST['latitud']),
                longitud =float(request.POST['longitud']),
            )
        
        if request.POST["action"] == 'delete_location':
            try:
                Ubicacion.objects.get(id=request.POST['location_id']).delete()
            except:
                pass
        
        if request.POST["action"] == 'update_settings':
            try:
                Tarifas.objects.all().delete()
                Tarifas.objects.create(
                    toneladas_seis = request.POST['tarifa6Tn'],
                    toneladas = request.POST['tarifaTn'],
                    toneladas_diez = request.POST['tarifa10Tn'],
                    kilogramos = request.POST['tarifaKg'],
                    libras = request.POST['tarifaLb'],
                )
            except:
                Tarifas.objects.all().delete()
                Tarifas.objects.create(
                    toneladas_seis = 0,
                    toneladas = 0,
                    toneladas_diez = 0,
                    kilogramos = 0,
                    libras = 0,
                )


    locations_json = []
    locations = Ubicacion.objects.all()
    for location in locations:
        locations_json.append(model_to_dict(location))

    tarifas = Tarifas.objects.last()
    
    
    context['gkey'] = MAP_KEY
    context['locations'] = locations_json
    try:
        context['tarifas'] = model_to_dict(tarifas)
    except:
        context['tarifas'] = {}
    
    return render(request, 'Zeus/v2/settings.html', context)



@login_required(login_url="/login")
def view_order_documents(request, order_id):
    context = {}
    try:
        order = Order.objects.get(id=order_id)
        context['order'] = model_to_dict(order)
        context['order']['status'] = ORDER_STATUS[order.status]
        context['order']['client'] = model_to_dict(order.client)
        context['order']['driver'] = model_to_dict(order.driver)
        context['order']['truck'] = model_to_dict(order.truck)

        archivos = OrdersFile.objects.filter(orden=order)
        file_names = []
        for archivo in archivos:

            file_names.append(model_to_dict(archivo.archivo))
        
        context['order']['files'] = file_names

    except Exception as e:
        context['error_message'] = 'No se pudo obtener la orden ' + str(order_id)
        print('-'*10)
        print(e)
        return render(request, 'Zeus/v2/error-page.html', context)
        print('-'*10)

    return render(request, 'Zeus/v2/order-file.html', context)

@login_required(login_url="/login")
def cancel_order(request, order_id):
    context = {}
    if request.method =='POST':
        try:
            order_id = request.POST["order"]
            order = Order.objects.get(id=order_id)
            order.status = 'CN'
            order.save()
        except:
            context['error_message'] = 'No se pudo obtener la orden ' + str(order_id)
            return render(request, 'Zeus/v2/error-page.html', context)
        
        return redirect('orders')
    else:
        order = Order.objects.get(id=order_id)
        context['order'] = model_to_dict(order)
        context['order']['status'] = ORDER_STATUS[order.status]
        return render(request, 'Zeus/v2/cancel-order.html', context)


@login_required(login_url="/login")
def reportes(request):
    context = {}
    if request.method =='POST':
        reporte_date = request.POST["daterange"]
        dates = reporte_date.split('-')
        start = dates[0].replace(' ','')
        end = dates[1].replace(' ','')

    else:
        now = datetime.date.today()
        start = now.strftime("%m/%d/%Y")
        end = now.strftime("%m/%d/%Y")
    
    context['start'] = start
    context['end'] = end

    start_date = datetime.datetime.strptime(start, "%m/%d/%Y")
    end_date = datetime.datetime.strptime(end, "%m/%d/%Y")


    revenue = {}

    list_orders = Order.objects.filter(creation_date__gte=start_date, creation_date__lte=end_date)
    ordenes_pendientes = list_orders.filter(status='PD')
    ordenes_proceso = list_orders.filter(status='EP')
    ordenes_finalizado = list_orders.filter(status='FN')
    ordenes_cancelado = list_orders.filter(status='CN')

    context['ordenes_pendientes'] = ordenes_pendientes
    context['ordenes_proceso'] = ordenes_proceso
    context['ordenes_finalizado'] = ordenes_finalizado
    context['ordenes_cancelado'] = ordenes_cancelado

    total_revenue = 0
    total_distance = 0
    total_ordenes_finalizadas = 0

    list_orders_json = []
    for order in list_orders:
        filtered_order = model_to_dict(order)
        filtered_order['creation_date'] = order.creation_date
        list_orders_json.append(filtered_order)
        day_date = str(order.creation_date.date())
        if order.status == 'FN':
            if order.precio:
                if day_date in revenue.keys():
                    revenue[day_date] = revenue[day_date] + order.precio
                    print('hello => ' , day_date)
                else:
                    print('hello => ' , day_date)
                    revenue[day_date] = order.precio
                
                total_revenue += order.precio
                total_distance += order.distancia
                total_ordenes_finalizadas += 1
    
    print('=>', revenue)

    context['fechas'] = revenue.keys()
    context['valores'] = revenue.values()
    context['order_list'] = list_orders_json

    context['total_revenue'] = float("{:.2f}".format(total_revenue))
    context['total_distance'] = float("{:.2f}".format(total_distance))
    context['total_ordenes_finalizadas'] = total_ordenes_finalizadas


    return render(request, 'Zeus/v2/reportes.html', context)

@login_required(login_url="/login")
def reporte_vehiculos(request):
    context = {}

    camiones = Truck.objects.all()
    camiones_disponibles = []
    camiones_mantenimiento = []
    camiones_inactivos = []

    for camion in camiones:
        camion_json = model_to_dict(camion)
        if camion.user:
            camion_json['user'] = model_to_dict(camion.user)
        

        if camion.is_active == False:
            camiones_inactivos.append(camion_json)
        else:
            if camion.status == 'Disponible':
                camiones_disponibles.append(camion_json)
            elif camion.status == 'En Mantenimiento':
                camiones_mantenimiento.append(camion_json)

    context['camiones_disponibles'] = camiones_disponibles
    context['camiones_mantenimiento'] = camiones_mantenimiento
    context['camiones_inactivos'] = camiones_inactivos
    
    return render(request, 'Zeus/v2/reporte-vehiculos.html', context)


@login_required(login_url="/login")
def reporte_conductores(request):
    context = {}
    if request.method =='POST':
        reporte_date = request.POST["daterange"]
        driver = request.POST["driver"]
        dates = reporte_date.split('-')
        start = dates[0].replace(' ','')
        end = dates[1].replace(' ','')

    else:
        now = datetime.date.today()
        start = now.strftime("%m/%d/%Y")
        end = now.strftime("%m/%d/%Y")
        driver = '00'

    list_active_drivers = []
    list_inactive_drivers = []
    selected_user = None

    usuarios = User.objects.all()
    for user in usuarios:
        rol = Rol.objects.filter(user=user, user_rol='DR').first()
        if rol:
            if rol.user.is_active:
                list_active_drivers.append(model_to_dict(rol.user))
            else:
                list_inactive_drivers.append(model_to_dict(rol.user))

                
    if driver != '00':
        selected_user = User.objects.filter(id=int(driver)).first()
    
    
    context['start'] = start
    context['end'] = end

    start_date = datetime.datetime.strptime(start, "%m/%d/%Y")
    end_date = datetime.datetime.strptime(end, "%m/%d/%Y")

    resume_drivers = []
    if selected_user:
        selected_user_json =model_to_dict(selected_user)
        list_orders = Order.objects.filter(creation_date__gte=start_date, creation_date__lte=end_date, driver=selected_user)
        ordenes_pendientes = len(list_orders.filter(status='PD'))
        ordenes_finalizado = len(list_orders.filter(status='FN'))
        ordenes_cancelado = len(list_orders.filter(status='CN'))
        ordenes_proceso = len(list_orders.filter(status='EP'))

        conductor_info = {
            'estado': selected_user_json['is_active'],
            'nombre': selected_user_json['first_name'] + ' ' + selected_user_json['last_name'],
            'ordenes_proceso': ordenes_proceso,
            'ordenes_pendientes': ordenes_pendientes,
            'ordenes_finalizado': ordenes_finalizado,
            'ordenes_cancelado': ordenes_cancelado,
        }
        resume_drivers.append(conductor_info)

    else:
        for conductor in list_active_drivers+list_inactive_drivers:
            user = User.objects.get(id=conductor['id'])
            list_orders = Order.objects.filter(creation_date__gte=start_date, creation_date__lte=end_date, driver=user)
            ordenes_pendientes = len(list_orders.filter(status='PD'))
            ordenes_finalizado = len(list_orders.filter(status='FN'))
            ordenes_cancelado = len(list_orders.filter(status='CN'))
            ordenes_proceso = len(list_orders.filter(status='EP'))

            conductor_info = {
                'estado': conductor['is_active'],
                'nombre': conductor['first_name'] + ' ' + conductor['last_name'],
                'ordenes_proceso': ordenes_proceso,
                'ordenes_pendientes': ordenes_pendientes,
                'ordenes_finalizado': ordenes_finalizado,
                'ordenes_cancelado': ordenes_cancelado,
            }
            resume_drivers.append(conductor_info)
            

    if selected_user:
        list_orders = Order.objects.filter(creation_date__gte=start_date, creation_date__lte=end_date, driver=selected_user)
    else:
        list_orders = Order.objects.filter(creation_date__gte=start_date, creation_date__lte=end_date)

    ordenes_pendientes = list_orders.filter(status='PD')
    ordenes_proceso = list_orders.filter(status='EP')
    ordenes_finalizado = list_orders.filter(status='FN')
    ordenes_cancelado = list_orders.filter(status='CN')

    context['ordenes_pendientes'] = ordenes_pendientes
    context['ordenes_proceso'] = ordenes_proceso
    context['ordenes_finalizado'] = ordenes_finalizado
    context['ordenes_cancelado'] = ordenes_cancelado

    revenue={}

    total_revenue = 0
    total_distance = 0
    total_ordenes_finalizadas = 0

    list_orders_json = []
    for order in list_orders:
        list_orders_json.append(model_to_dict(order))
        day_date = str(order.creation_date.date())
        if order.status == 'FN':
            if order.precio:
                if day_date in revenue.keys():
                    revenue[day_date] = revenue[day_date] + order.precio
                else:
                    revenue[day_date] = order.precio
                
                total_revenue += order.precio
                total_distance += order.distancia
                total_ordenes_finalizadas += 1
    

    context['fechas'] = revenue.keys()
    context['valores'] = revenue.values()
    context['order_list'] = list_orders_json

    context['total_revenue'] = float("{:.2f}".format(total_revenue))
    context['total_distance'] = float("{:.2f}".format(total_distance))
    context['total_ordenes_finalizadas'] = total_ordenes_finalizadas

    context['list_active_drivers'] = list_active_drivers
    context['list_inactive_drivers'] = list_inactive_drivers
    context['resume_drivers'] = resume_drivers


    return render(request, 'Zeus/v2/reporte-conductores.html', context)



def recuperar_contrasena(request):
    context = {}
    if request.method =='POST':
        email = request.POST["email"]
        edit_user = User.objects.filter(email=email).first()

        if edit_user is None:
            context['error'] = True
            context['error_message'] = 'El usuario no se encuentra en la base de datos'
            return render(request, 'Zeus/v2/recuperar-contrasena.html', context)

        
        context['success'] = True
        context['success_message'] = 'Se envio un correo con un link para el cambio de contrasena'

        secret_token = hashlib.new('sha256')
        secret_token.update(edit_user.username.encode('utf-8'))

        change_password = changePasswordToken.objects.create(
            user=edit_user,
            cp_token=secret_token.hexdigest()
        )
        url = f'{SITE_URL}/cambio-clave/{change_password.cp_token}/'
        message = 'Para cambiar su contrasena de click en el siguiente enlace: \n' + url

        try:
            email = EmailMessage('Cambio de contrasena', message, to=[email])
            email.send()
        except:
            context['error'] = True
            context['error_message'] = 'No se pudo enviar el correo a ' + email
            return render(request, 'Zeus/v2/recuperar-contrasena.html', context)
        
        context['method'] = 'POST'

    else:

        context['method'] = 'get maybe'

    return render(request, 'Zeus/v2/recuperar-contrasena.html', context)


def cambio_clave(request, token):
    context = {}

    if request.method =='POST':
        token = request.POST["token"]
        contrasena = request.POST["contrasena"]
        change_password = changePasswordToken.objects.filter(cp_token=token).first()

        edit_user = change_password.user
        edit_user.set_password(contrasena)
        edit_user.save()

        change_password = changePasswordToken.objects.filter(cp_token=token).delete()
        return redirect('login')

    else:
        try:
            change_password = changePasswordToken.objects.filter(cp_token=token).first()
            context['token'] = change_password.cp_token
        except Exception as e:
            print(e)
            context['error'] = True
            context['error_message'] = "El token ha expirado"

    return render(request, 'Zeus/v2/cambio-clave.html', context)
    

@login_required(login_url="/login")
def ordenes_completas(request):
    context = {}
    order_list = Order.objects.filter(status__in=['FN', 'CN']).order_by('creation_date').reverse()
    order_list_json = []
    for order in order_list:
        order_json = model_to_dict(order)
        order_json['client'] = order.client.first_name + ' ' + order.client.last_name
        order_json['admin'] = order.responsible.first_name + ' ' + order.responsible.last_name
        order_json['driver'] = order.driver.first_name + ' ' + order.driver.last_name
        order_json['truck'] = order.truck.brand + ' - ' + order.truck.license
        order_json['status'] = ORDER_STATUS[order.status]
        order_list_json.append(order_json)
    
    context['view_title'] = 'Ordenes Finalizadas o Canceladas'
    context['order_list'] = order_list_json
    return render(request, 'Zeus/v2/order-list.html', context)

@login_required(login_url="/login")
def ver_formulario(request, order_id):
    context = {}

    formulario = Formulario.objects.filter(orden=order_id).first()
    formulario_json = None
    if formulario:
        formulario_json = model_to_dict(formulario)
        formulario_json['foto'] = model_to_dict(formulario.foto)
    
    context['formulario'] = formulario_json
    print(formulario_json)

    return render(request, 'Zeus/v2/ver-formulario.html', context)

