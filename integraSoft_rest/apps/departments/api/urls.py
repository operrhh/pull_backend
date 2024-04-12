from django.urls import path
from .api import (
    departments_hcm_api_view,
    departments_peoplesoft_api_view
)

urlpatterns = [
    path('hcm/', departments_hcm_api_view, name = 'departments_hcm_api'),
    path('peoplesoft/', departments_peoplesoft_api_view, name = 'departments_peoplesoft_api'),
]