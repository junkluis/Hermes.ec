from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from .serializers import UserSerializer, GroupSerializer
from Heraldo.models import Rol, Driver, DriverStatus, Truck, Order
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.forms.models import model_to_dict

from Zeus.constants import USER_ROL



def index(request):
    return HttpResponse("La más dulce vida consiste en no saber nada.")

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET', 'POST'])
def hello_world(request):
    if request.method == 'POST':
        return Response({"message": "Got some data!", "data": request.data})
    return Response({"message": "Hello, world!"})

@api_view(['GET', 'POST'])
def user_information(request):
    context = {}
    if request.method == 'POST':
        username = request.data.get('username')
        user = User.objects.filter(username=username)
        if len(user) == 0:
            context['error'] = True
            context['error_message'] = 'User not found'
            return Response(context)

        user_info = user.first()

        context['username'] = user_info.username
        context['email'] = user_info.email
        context['first_name'] = user_info.first_name
        context['last_name'] = user_info.last_name
        context['last_login'] = user_info.last_login

        user_rol = Rol.objects.filter(user=user_info)
        
        if len(user_rol) == 0:
            context['rol'] = USER_ROL['NN']
        else:
            context['rol'] =  USER_ROL[user_rol.first().user_rol]

        if user_rol.first().user_rol == 'DR':
            context['trucks'] = []
            trucks = Truck.objects.filter(user=user_info)
            list_trucks = []
            if len(trucks) > 0:
                for truck in trucks:
                    list_trucks.append(model_to_dict(truck))
                context['trucks'] = list_trucks

        return Response(context)
    
    context['Message'] = 'Endpoint obtiene la informacion del usuario'
    return Response(context)


@api_view(['GET', 'POST'])
def get_orders(request):
    context = {}
    if request.method == 'POST':
        username = request.data.get('username')
        user = User.objects.filter(username=username)

        if len(user) == 0:
            context['error'] = True
            context['error_message'] = 'User not found'
            return Response(context)
        
        user_info = user.first()
        user_rol = Rol.objects.filter(user=user_info)
        if len(user_rol) == 0:
            context['error'] = True
            context['error_message'] = 'Invalid Rol'
            return Response(context)

        else:
            rol = user_rol.first().user_rol
            if rol == 'DR':
                order_list = Order.objects.filter(driver=user_info)
            elif rol == 'CL':
                order_list = Order.objects.filter(client=user_info)

            else:
                context['error'] = True
                context['error_message'] = 'Invalid Rol'
                return Response(context)
            
            order_list_json = []
            for order in order_list:
                order_json = model_to_dict(order)
                order_json['responsible'] = { 
                    'identification': order.responsible.username,
                    'full_name': order.responsible.first_name + '' + order.responsible.last_name,
                    }
                order_json['driver'] = { 
                    'identification': order.driver.username,
                    'full_name': order.driver.first_name + '' + order.driver.last_name,
                }
                order_json['client'] = { 
                    'identification': order.client.username,
                    'full_name': order.client.first_name + '' + order.client.last_name,
                }
                order_json['truck'] = model_to_dict(order.truck)
                order_list_json.append(order_json)
            
            context['orders'] = order_list_json
        return Response(context)
    
    context['Message'] = 'Endpoint obtiene la informacion de ordenes'
    return Response(context)