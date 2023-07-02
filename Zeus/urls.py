from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_zeus, name="login"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("users", views.users, name="users"),
    path("trucks", views.trucks, name="trucks"),
    path("orders", views.orders, name="orders"),
    path("new_user", views.new_user, name="new_user"),
    path("new_truck", views.new_truck, name="new_truck"),
    path("delete/<str:object>/<int:key_id>", views.delete, name="delete"),
    path("edit/<str:object>/<int:key_id>", views.edit, name="edit"),
    path("reactivate/<str:object>/<int:key_id>", views.reactivate, name="reactivate"),
    path("view_orders/<str:order_id>", views.view_orders, name="view_orders"),
    path("cancelar/<str:order_id>", views.cancel_order, name="cancel_order"),

    path("view_order_documents/<str:order_id>", views.view_order_documents, name="view_order_documents"),
    path("new_order", views.new_order, name="new_order"),
    path("hermes_settings", views.hermes_settings, name="hermes_settings"),

    

    path("logout", views.logout_zeus, name="logout"),
    path("not_implemented", views.not_implemented, name="not_implemented"),
    

    path("donwload_users", views.donwload_users, name="donwload_users"),
    path("donwload_truck", views.donwload_truck, name="donwload_truck"),


    path("dashboard_v2", views.dashboard_v2, name="dashboard_v2"),

    path("reportes", views.reportes, name="reportes"),

    path("recuperar_contrasena", views.recuperar_contrasena, name="recuperar_contrasena"),

    
    
    
]