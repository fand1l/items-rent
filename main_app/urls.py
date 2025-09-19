from django.urls import path
from . import views

app_name = "main_app"
urlpatterns = [
    path("", views.items, name="items"),
    path("items/<int:pk>/", views.item_det, name="items_det"),
    path("rentals/", views.rentals, name="rentals")
]