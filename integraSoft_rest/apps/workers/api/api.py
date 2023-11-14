#Librerias
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


#Paginations
from ..pagination import CustomPaginationPeopleSoft, CustomPaginationHcm

#Serializers
from .serializers import WorkerHcmSerializer, WorkerPeopleSoftSerializer

# Service
from ..services.workerServiceHcm import WorkerServiceHcm
from ..services.workerServicePeopleSoft import WorkerServicePeopleSoft

# region HCM
@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def workers_hcm_api_view(request):
    if request.method == 'GET':
        worker_service = WorkerServiceHcm()
        try:
            workers = worker_service.get_workers_hcm(request)
            if workers:
                pagination = CustomPaginationHcm()
                pagination.queryset = workers
                result_page = pagination.paginate_queryset(workers, request)
                if result_page is not None:
                    workers_serializer = WorkerHcmSerializer(result_page, many=True)
                    response = pagination.get_paginated_response(workers_serializer.data)
                    return Response(response.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)})

@api_view(['PUT'])
def worker_hcm_update_api_view(request,pk):
    if request.method == 'PUT':
        worker_service = WorkerServiceHcm()
        try:
            worker = worker_service.get_worker_hcm(pk)
            if worker:
                worker_serializer = WorkerHcmSerializer(worker)
                res = worker_service.update_worker_hcm(request.body, worker_serializer.data)
                return Response(res, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)
# endregion

# region PeopleSoft
@api_view(['GET'])
def workers_peoplesoft_api_view(request):
    if request.method == 'GET':
        print(request.user)
        print(request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1])        
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
def worker_peoplesoft_api_view(request,pk):
    if request.method == 'GET':
        worker_service = WorkerServicePeopleSoft()
        try:
            worker = worker_service.get_worker_peoplesoft(pk)
            if worker:
                worker_serializer = WorkerPeopleSoftSerializer(worker)
                return Response(worker_serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)
# endregion