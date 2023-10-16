from rest_framework.exceptions import APIException
from rest_framework import status

class ExceptionJson(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Json enviado invalido'
    default_code = 'invalid_json'

class ExceptionWorkerHcm(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Error al obtener worker en Hcm'
    default_code = 'error_worker_hcm'

class ExceptionWorkerPeopleSoft(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Error al obtener worker en PeopleSoft'
    default_code = 'error_worker_peoplesoft'

class ExceptionOracleDatabase(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Error al obtener worker en PeopleSoft'
    default_code = 'error_worker_peoplesoft'