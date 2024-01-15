from rest_framework.exceptions import APIException
from rest_framework import status

class ExceptionDepartmentHcm(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Error al obtener department en Hcm'
    default_code = 'error_department_hcm'

class ExceptionDepartmentPeopleSoft(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Error al obtener department en PeopleSoft'
    default_code = 'error_department_peoplesoft'