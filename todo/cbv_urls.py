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
    path("todo/", TodoListView.as_view(), name="cbv_todo_list"),
    path("todo/create/", TodoCreateView.as_view(), name="cbv_todo_create"),
    path("todo/<int:pk>/", TodoDetailView.as_view(), name="cbv_todo_info"),
    path("todo/<int:pk>/update/", TodoUpdateView.as_view(), name="cbv_todo_update"),
    path("todo/<int:pk>/delete/", TodoDeleteView.as_view(), name="cbv_todo_delete"),

    path(
        "todo/<int:todo_pk>/comments/create/",
        CommentCreateView.as_view(),
        name="cbv_comment_create",
    ),
    path(
        "comments/<int:pk>/update/",
        CommentUpdateView.as_view(),
        name="cbv_comment_update",
    ),
    path(
        "comments/<int:pk>/delete/",
        CommentDeleteView.as_view(),
        name="cbv_comment_delete",
    ),
]
