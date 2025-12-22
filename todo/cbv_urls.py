from django.urls import path
from .cb_views import (
    TodoListView,
    TodoDetailView,
    TodoCreateView,
    TodoUpdateView,
    TodoDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
)

urlpatterns = [
    path("", TodoListView.as_view(), name="cbv_todo_list"),
    path("todo/", TodoListView.as_view(), name="cbv_todo_list"), 

    path("create/", TodoCreateView.as_view(), name="cbv_todo_create"),
    path("<int:pk>/", TodoDetailView.as_view(), name="cbv_todo_info"),
    path("<int:pk>/update/", TodoUpdateView.as_view(), name="cbv_todo_update"),
    path("<int:pk>/delete/", TodoDeleteView.as_view(), name="cbv_todo_delete"),
    path("<int:pk>/comments/create/", CommentCreateView.as_view(), name="cbv_comment_create"),
    path("comment/<int:pk>/update/", CommentUpdateView.as_view(), name="cbv_comment_update"),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="cbv_comment_delete"),
]
