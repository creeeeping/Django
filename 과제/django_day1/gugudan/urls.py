from django.urls import path
from .views import gugudan_view

urlpatterns = [
    path('<int:num>/', gugudan_view),
]
