from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib import messages
from .models import CustomUser
from booking.models import Booking


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


@login_required
def put_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        phone_number = request.POST.get("phone_number")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        request.user.username = username
        request.user.phone_number = phone_number
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()
        return redirect("room-list")
    else:
        return render(request,
                      "auth_system/put_user.html")


def put_password_view(request):
    if request.method == "POST":
        password = request.POST.get("password")
        password_again = request.POST.get("password-again")
        if password == password_again:
            request.user.set_password(password)
            request.user.save()
            return redirect("room-list")
        else:
            messages.error(request, "Passwords aren't same.")

    return render(request,
                  "auth_system/put_password.html")


@login_required
def delete_view(request, continue_delete):
    if continue_delete == 0:
        return render(request,
                      "auth_system/delete_user.html")

    elif continue_delete == 1:
        request.user.delete()
        return redirect("register")


def user_details(request, pk):
    user = CustomUser.objects.get(pk=pk)
    bookings = Booking.objects.filter(user=user)
    context = {
        "user": user,
        "bookings": len(bookings),
    }
    return render(request,
                  "auth_system/user_details.html",
                  context)
