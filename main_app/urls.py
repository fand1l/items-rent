from django.urls import path
from . import views

app_name = "main_app"
urlpatterns = [
    path("", views.items_list, name="items_list"),
    path("items/<int:pk>/", views.items_detail, name="items_detail"),
    path("rentals/", views.my_rentals, name="my_rentals"),
    path("rentals/<int:pk>/cancel/", views.rental_cancel, name="rental_cancel"),
]