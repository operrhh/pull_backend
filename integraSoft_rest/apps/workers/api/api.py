#Librerias
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from ...custom_authentication import CustomTokenAuthentication

#Paginations
from ..pagination import CustomPaginationPeopleSoft

#Serializers
from .serializers import WorkerHcmSerializer, WorkersHcmSerializer, WorkerPeopleSoftSerializer, WorkersWsdlSerializer

# Services
from ..services.workerServiceHcm import WorkerServiceHcm
from ..services.workerServicePeopleSoft import WorkerServicePeopleSoft
from ..services.workerServiceWsdl import WorkerServiceWsdl
from ..services.worker_service_comparison import WorkerServiceComparison
from ..services.worker_service_comparison_excel import WorkerServiceComparisonExcel

# region HCM
@api_view(['GET', 'PUT', 'POST'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def workers_hcm_api_view(request):
    try:
        worker_service = WorkerServiceHcm()

        if request.method == 'GET':
            many_workers = request.query_params.get('manyWorkers', 'True').lower() == 'true'
            if many_workers:
                workers = worker_service.get_workers_hcm(request)
                if workers:
                    workers_serializer = WorkersHcmSerializer(workers)
                    return Response(workers_serializer.data, status = status.HTTP_200_OK)
            else:
                worker = worker_service.get_worker_hcm(request)
                if worker:
                        worker_serializer = WorkerHcmSerializer(worker)
                        return Response(worker_serializer.data, status = status.HTTP_200_OK)                
        if request.method == 'PUT':
            try:
                workers = worker_service.get_workers_hcm(request)
                if workers and len(workers) == 1:
                    worker = workers[0]
                    worker_serializer = WorkerHcmSerializer(worker)
                    res = worker_service.update_worker_hcm(request.body, worker_serializer.data)
                    return Response(res, status = status.HTTP_200_OK)
                else:
                    return Response({'message': 'La busqueda de Workers arrojo mas de un resultado'}, status = status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message': str(e)})
        if request.method == 'POST':
            try:
                res = worker_service.create_worker_hcm(request)
                return Response(res, status = status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': str(e)})            
    except Exception as e:
        return Response({'message': str(e)})

@api_view(['POST'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def workers_hcm_change_manager_api_view(request):
    try:
        worker_service = WorkerServiceHcm()
        if request.method == 'POST':
            try:
                res = worker_service.change_manager_hcm(request)
                return Response(res, status = status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def workers_hcm_update_assignment_name_api_view(request):
    try:
        worker_service = WorkerServiceHcm()
        if request.method == 'POST':
            try:
                res = worker_service.update_assignment_name_hcm(request)
                return Response(res, status = status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)

# endregion

# region PeopleSoft
@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def workers_peoplesoft_api_view(request):
    if request.method == 'GET':
        worker_service = WorkerServicePeopleSoft()
        try:
            workers = worker_service.get_workers_peoplesoft(request)
            if workers:
                pagination = CustomPaginationPeopleSoft()
                pagination.queryset = workers
                result_page = pagination.paginate_queryset(workers, request)
                if result_page is not None:
                    workers_serializer = WorkerPeopleSoftSerializer(result_page, many=True)
                    response = pagination.get_paginated_response(workers_serializer.data)
                    return Response(response.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def worker_peoplesoft_api_view(request,pk):
    if request.method == 'GET':
        worker_service = WorkerServicePeopleSoft()
        try:
            worker = worker_service.get_worker_peoplesoft(request, pk)
            if worker:
                worker_serializer = WorkerPeopleSoftSerializer(worker)
                return Response(worker_serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)
# endregion

# region WSDL
@api_view(['GET'])
def workers_wsdl_api_view(request):
    try:
        worker_service = WorkerServiceWsdl()
        if request.method == 'GET':
            workers = worker_service.get_workers_wsdl()
            if workers:
                workers_serializer = WorkersWsdlSerializer(workers)
                return Response(workers_serializer.data, status = status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': str(e)})

# endregion

# region Comparison
@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def workers_comparison_api_view(request):
    try:
        worker_service = WorkerServiceComparison()
        if request.method == 'GET':
            workers = worker_service.get_workers_comparison(request)
            if workers:
                return Response(workers, status = status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': str(e)})

@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def workers_comparison_excel_api_view(request):
    try:
        worker_service = WorkerServiceComparisonExcel()
        if request.method == 'GET':
            return worker_service.run(request=request)
    except Exception as e:
        return Response({'message': str(e)})

# endregion