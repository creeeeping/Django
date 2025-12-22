from django.contrib import admin
from .models import Todo, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "is_completed", "start_date", "end_date")
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "todo", "user", "message", "created_at")
    ordering = ("-created_at",)
