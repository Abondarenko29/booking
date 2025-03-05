from django.urls import path
from .views import register, logout_view, login_view, user_details
from .views import put_view, put_password_view, delete_view


urlpatterns = [
    path("register/", register, name="register"),
    path("logout/", logout_view, name="logout"),
    path("login/", login_view, name="login"),
    path("put/", put_view, name="put"),
    path("delete/<int:continue_delete>", delete_view, name="delete"),
    path("put/password/", put_password_view, name="put-password"),
    path("user/<int:pk>", user_details, name="user-details")
]
