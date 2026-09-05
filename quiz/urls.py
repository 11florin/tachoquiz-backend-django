from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("confirmation/", views.confirmation, name="confirmation"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("quiz/", views.quiz_view, name="quiz"),
    path("score/", views.score_view, name="score"),

]