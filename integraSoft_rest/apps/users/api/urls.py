from django.urls import path
from .api import user_api_view,user_detail_api_view,user_create_api_view

urlpatterns = [
    path('', user_api_view, name = 'usuario_api'),
    path('create/', user_create_api_view, name = 'usuario_create_api'),
    path('<int:pk>/', user_detail_api_view, name = 'usuario_detail_api'),
]