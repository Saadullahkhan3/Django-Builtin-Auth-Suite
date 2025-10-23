from django.urls import path
from . import views

urlpatterns = [
    path("@<str:username>/", views.user_profile, name="user_profile"),
    path("register/", views.user_register, name="register"),
    path("login/", views.user_login, name="login"),
    path("update/", views.user_update, name="user_update"),
    path("delete/", views.user_delete, name="user_delete"),
    path("password_update/", views.user_password_update, name="user_password_update"),
    path("password_reset/", views.user_password_reset, name="user_password_reset"),
    path("confirm-logout/", views.confirm_logout, name="confirm-logout"),
]
