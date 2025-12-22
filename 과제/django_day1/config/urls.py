from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include('movies.urls')),
    path('books/', include('books.urls')),
    path('gugudan/', include('gugudan.urls')),
]
