from django.contrib import admin
from .models import Item, Rental, DamageReport

# Register your models here.
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price_per_day", "deposit", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ("user", "item", "start_date", "end_date", "status", "total_price", "deposit_amount")
    list_filter = ("status", "total_price", "deposit_amount")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("start_date", "end_date")


@admin.register(DamageReport)
class DamageReportAdmin(admin.ModelAdmin):
    list_display = ("rental", "note", "fee", "created_at")
    list_filter = ("note", "created_at")
    search_fields = ("note",)
    readonly_fields = ("created_at",)
