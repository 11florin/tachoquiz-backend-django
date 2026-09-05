from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("confirmation/", views.confirmation, name="confirmation"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.login_view, name="logout"),
]