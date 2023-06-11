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
    path("new_order", views.not_implemented, name="not_implemented"),
    path("delete/<str:object>/<int:key_id>", views.delete, name="delete"),
    path("edit/<str:object>/<int:key_id>", views.edit, name="edit"),
    path("reactivate/<str:object>/<int:key_id>", views.reactivate, name="reactivate"),
    path("logout", views.logout_zeus, name="logout"),
    path("not_implemented", views.not_implemented, name="not_implemented"),

    path("donwload_users", views.donwload_users, name="donwload_users"),
    path("donwload_truck", views.donwload_truck, name="donwload_truck"),
    
]