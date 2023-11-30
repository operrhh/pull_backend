from django.urls import path
from .api import (
    workers_hcm_api_view,
    workers_peoplesoft_api_view,
    worker_peoplesoft_api_view
)

urlpatterns = [
    path('hcm/', workers_hcm_api_view, name = 'workers_hcm_api'),
    path('peoplesoft/', workers_peoplesoft_api_view, name='workers_peoplesoft_api'),
    path('peoplesoft/<str:pk>/', worker_peoplesoft_api_view, name='worker_peoplesoft_api'),
]