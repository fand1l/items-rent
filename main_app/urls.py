from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "main_app"

urlpatterns = [
    path("", views.items_list, name="items_list"),
    path("items/<int:pk>/", views.items_detail, name="items_detail"),
    path("rentals/", views.my_rentals, name="my_rentals"),
    path("rentals/<int:pk>/cancel/", views.rental_cancel, name="rental_cancel"),

    path("account/register", views.register, name="register"),
    path("account/login", auth_views.LoginView.as_view(template_name="main_app/auth/login.html"), name="login"),
    path("account/logout", auth_views.LogoutView.as_view(), name="logout")
]