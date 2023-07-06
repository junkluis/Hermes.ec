from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path("saludos", views.index, name="index"),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('hello_world', views.hello_world, name='hello'),
    path('user_information', views.user_information, name='user_information'),
    path('get_orders', views.get_orders, name='get_orders'),
    path('get_active_order', views.get_active_order, name='get_active_order'), 
    path('update_order', views.update_order, name='update_order'), 
    path('update_truck_location', views.update_truck_location, name='update_truck_location'),
    path('order_location', views.order_location, name='order_location'), 

    path('informar_imprevisto', views.informar_imprevisto, name='informar_imprevisto'), 
    path('confirmar_entrega', views.confirmar_entrega, name='confirmar_entrega'),

    
    
]
