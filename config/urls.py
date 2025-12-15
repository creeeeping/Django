from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("", lambda request: redirect("todo/")),
    path("admin/", admin.site.urls),
    path("todo/", include("todo.urls")),
]
