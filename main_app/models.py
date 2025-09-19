from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import F, Q


# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    class Meta:
        abstract = True


class Item(models.Model):
    CATEGORY_CHOICES = [
        ("camera", "Camera"),
        ("tripod", "Tripod"),
        ("drone", "Drone"),
    ]
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    deposit = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "item"
        verbose_name = "Предмет"
        verbose_name_plural = "Предмети"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["category"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name


class Rental(TimeStampedModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("active", "Active"),
        ("returned", "Returned"),
        ("cancelled", "Cancelled"),
        ("overdue", "Overdue"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(choices=STATUS_CHOICES, default="pending", max_length=20)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "rental"
        verbose_name = "Оренда"
        verbose_name_plural = "Оренди"
        ordering = ["status"]
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["item", "start_date"]),
            models.Index(fields=["item", "end_date"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.status

    
class DamageReport(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    note = models.TextField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.note
    
