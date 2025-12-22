from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .cb_views import (
    TodoListView, TodoDetailView,
    CommentCreateView, CommentUpdateView, CommentDeleteView
)

urlpatterns = [
    path('todo/', TodoListView.as_view(), name='cbv_todo_list'),
    path('todo/<int:pk>/', TodoDetailView.as_view(), name='cbv_todo_info'),

    path('comment/<int:todo_id>/create/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)