from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm
from django.contrib import messages


# Create your views here.
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("room-list")
    else:
        form = CustomUserCreationForm()
        messages.error(request, "Incorrecet data.")
    context = {
        "form": form,
    }
    return render(request,
                  "auth_system/register.html",
                  context)


def logout_view(request):
    logout(request)
    return redirect("login")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("room-list")
        else:
            messages.error(request, "Неправильний username чи пароль")
    return render(request,
                  "auth_system/login.html")
