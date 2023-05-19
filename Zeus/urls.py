from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_zeus, name="login"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("users", views.users, name="users"),
    path("new_user", views.new_user, name="new_user"),
    path("logout", views.logout_zeus, name="logout"),
    path("not_implemented", views.not_implemented, name="not_implemented"),
    
]