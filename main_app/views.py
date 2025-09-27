from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, F
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import RentalForm
from .models import Item, Rental, DamageReport

# Create your views here.
def items_list(request):
    items = Item.objects.select_related().order_by("name").filter(is_active=True)
    q = request.GET.get("q", "").strip()
    cat = request.GET.get("cat", "").strip()

    if q:
        items = items.filter(name__icontains=q)
    if cat:
        items = items.filter(category=cat)

    categories = Item.objects.filter(is_active=True).values_list("category", flat=True).distinct().order_by("category")

    ctx = {"items": items, "categories": categories, "q": q, "cat": cat}
    return render(request, "main_app/items_list.html", ctx)


def items_detail(request, pk: int):
    item = get_object_or_404(Item.objects.select_related(), pk=pk, is_active=True)

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "Увійдіть, щоб орендувати предмет.")
            return redirect(reverse("main_app:items_detail", args=[item.pk]))
        instance = Rental(item=item, user=request.user)
        form = RentalForm(request.POST, instance=instance)
        if form.is_valid():
            rental = form.save(commit=False)
            days = (rental.end_date - rental.start_date).days + 1
            rental.total_price = days * item.price_per_day
            rental.deposit_amount = item.deposit
            rental.save()
            messages.success(request, "Заявка створена! Очікує підтвердження.")
            return redirect("main_app:my_rentals")
    else:
        form = RentalForm()

    last_rentals = item.rental_set.select_related("user").order_by("-created_at")[:5]
    ctx = {"item": item, "form": form, "last_rentals": last_rentals}
    return render(request, "main_app/items_detail.html", ctx)


@login_required
def my_rentals(request):
    rentals = Rental.objects.select_related("item").filter(user=request.user).order_by("-created_at")
    return render(request, "main_app/my_rentals.html", {"rentals": rentals})


@login_required
def rental_cancel(request, pk: int):
    rental = get_object_or_404(Rental, pk=pk, user=request.user)
    if rental.status != "cancelled":
        rental.status = "cancelled"
        rental.save()
        messages.info(request, "Оренду скасовано.")
    return redirect("main_app:my_rentals")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Обліковий запис створено")
            return redirect("main_app:items_list")
        
    else:
        form = UserCreationForm()

    return render(request, "main_app/auth/register.html", {"form":form})