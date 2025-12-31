from django.contrib import admin
from restaurants.models import Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address", "contact", "regular_holiday", "created_at", "updated_at")
    search_fields = ("name", "address", "contact")
    list_filter = ("regular_holiday",)
