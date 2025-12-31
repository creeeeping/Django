from django.contrib import admin
from django.urls import path, include
from restaurants.urls import router as restaurants_router

urlpatterns = [
    path("admin/", admin.site.urls),

    # users
    path("users/", include("users.urls")),

    # reviews (요구사항: include 방식)
    path("", include("reviews.urls")),

    # restaurants (기존 router)
    path("", include(restaurants_router.urls)),
]
