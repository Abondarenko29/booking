from django.urls import path
from .views import register, logout_view, login_view
from .views import put_view, delete_view


urlpatterns = [
    path("register/", register, name="register"),
    path("logout/", logout_view, name="logout"),
    path("login/", login_view, name="login"),
    path("put/", put_view, name="put"),
    path("delete/<int:continue_delete>", delete_view, name="delete"),
]
