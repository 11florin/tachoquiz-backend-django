from django.shortcuts import render
from .forms import RegistrationForm


# Create your views here.
def home(request):
    return render(request, "quiz/home.html")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()

    else:
        form = RegistrationForm()

    return render(request, "quiz/register.html", {"form": form})