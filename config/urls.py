from django.contrib import admin
from django.urls import path, include
from restaurants.urls import router as restaurants_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(restaurants_router.urls)),
]
