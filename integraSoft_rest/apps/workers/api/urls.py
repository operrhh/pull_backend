from django.urls import path
from .api import (
    workers_hcm_api_view,
    workers_peoplesoft_api_view,
    worker_peoplesoft_api_view,
    workers_wsdl_api_view,
    workers_comparison_api_view,
    workers_comparison_excel_api_view,
    workers_hcm_change_manager_api_view,
    workers_hcm_update_assignment_name_api_view
)

urlpatterns = [
    path('hcm/', workers_hcm_api_view, name = 'workers_hcm_api'),
    path('hcm/changeManager/', workers_hcm_change_manager_api_view, name = 'workers_hcm_change_manager_api'),
    path('hcm/updateAssignmentName/', workers_hcm_update_assignment_name_api_view, name = 'workers_hcm_update_assignment_name_api'),
    path('peoplesoft/', workers_peoplesoft_api_view, name='workers_peoplesoft_api'),
    path('peoplesoft/<str:pk>/', worker_peoplesoft_api_view, name='worker_peoplesoft_api'),
    path('wsdl/', workers_wsdl_api_view, name='workers_wsdl_api'),
    path('comparison/', workers_comparison_api_view, name='workers_comparison_api'),
    path('comparison/excel/', workers_comparison_excel_api_view, name='workers_comparison_excel_api')
]