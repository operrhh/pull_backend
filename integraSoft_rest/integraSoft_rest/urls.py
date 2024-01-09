"""integraSoft_rest URL Configuration
PRUEBA NUEVA CONEX
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.users.api.api import user_login_api_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", user_login_api_view, name="user_login_api_view"),
    path('worker/', include('apps.workers.api.urls')),
    path('user/', include('apps.users.api.urls')),
    path('parameter/', include('apps.parameters.api.urls')),
]
