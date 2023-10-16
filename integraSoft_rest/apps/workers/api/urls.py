from django.urls import path
from .api import worker_hcm_update_api_view, worker_hcm_detail_api_view, worker_hcm_api_view,worker_peoplesoft_api_view

urlpatterns = [
    path('hcm/', worker_hcm_api_view, name = 'worker_hcm_api'),
    path('hcm/<str:pk>/', worker_hcm_detail_api_view, name='worker_hcm_detail_api'),
    path('hcm/<str:pk>/update/', worker_hcm_update_api_view, name='worker_hcm_update_api'),
    path('peoplesoft/', worker_peoplesoft_api_view, name='worker_peoplesoft_api')
]