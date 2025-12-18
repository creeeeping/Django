from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_completed', 'created_at')
    search_fields = ('title', 'description', 'user__username')
