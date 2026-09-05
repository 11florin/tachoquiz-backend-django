from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegistrationForm


# Create your views here.
def home(request):
    return render(request, "quiz/home.html")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("confirmation")

    else:
        form = RegistrationForm()

    return render(request, "quiz/register.html", {"form": form})


def confirmation(request):
    return render(request, "quiz/confirmation.html")



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "quiz/login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "quiz/login.html")



def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def quiz_view(request):
    return render(request, "quiz/quiz.html")


@login_required
def score_ciew(request):
    return render(request, "quiz/score.html")