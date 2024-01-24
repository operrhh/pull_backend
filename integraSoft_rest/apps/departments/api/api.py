from ...custom_authentication import CustomTokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

# Decorators
from rest_framework.decorators import api_view, permission_classes, authentication_classes

#Paginations
from ..pagination import CustomPaginationPeopleSoft

# Services
from ..services.departmentServiceHcm import DepartmentServiceHcm
from ..services.departmentServicePeopleSoft import DepartmentServicePeopleSoft

# Serializers
from .serializers import DepartmentHcmSerializer, DepartmentSerializer


# HCM

@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([AllowAny])
def departments_hcm_api_view(request):
    try:
        department_service = DepartmentServiceHcm()
        if request.method == 'GET':
            departments = department_service.get_departments(request)
            if departments:
                departments_serializer = DepartmentHcmSerializer(departments)
                return Response(departments_serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': str(e)})


# PeopleSoft

@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([AllowAny])
def departments_peoplesoft_api_view(request):
    try:
        department_service = DepartmentServicePeopleSoft()

        if request.method == 'GET':
            departments = department_service.get_departments(request)
            if departments:
                pagination = CustomPaginationPeopleSoft()
                pagination.queryset = departments
                result_page = pagination.paginate_queryset(departments, request)
                if result_page is not None:
                    departments_serializer = DepartmentSerializer(result_page, many=True)
                    response = pagination.get_paginated_response(departments_serializer.data)
                    return Response(response.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': str(e)})