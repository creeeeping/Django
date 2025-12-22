from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from users.views import sign_up

urlpatterns = [
    path('', lambda r: redirect('cbv/todo/')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', sign_up, name='signup'),
    path('cbv/', include('todo.cbv_urls')),
]
