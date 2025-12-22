from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Todo, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Todo)
class TodoAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display = ("id", "user", "title", "is_completed", "created_at")
    fieldsets = (
        ('Todo', {
            'fields': (
                'user',
                'title',
                'description',
                'thumbnail',
                'completed_image',
                'is_completed',
                'start_date',
                'end_date',
            )
        }),
    )
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "todo", "user", "content", "created_at")
