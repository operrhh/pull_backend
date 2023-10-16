from django.urls import path
from .api import parameter_api_view,parameter_detail_api_view, parameterType_api_view, parameterType_detail_api_view

urlpatterns = [
    path('', parameter_api_view, name = 'parameter_api'),
    path('<int:pk>/', parameter_detail_api_view, name = 'parameter_detail_api'),
    path('parameterType/', parameterType_api_view, name = 'parameter_api'),
    path('parameterType/<int:pk>/', parameterType_detail_api_view, name = 'parameter_detail_api'),
]