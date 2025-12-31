from django.contrib import admin
from reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "restaurant", "user", "title", "created_at", "updated_at")
    search_fields = ("title", "comment", "restaurant__name", "user__email")
    list_filter = ("restaurant",)
