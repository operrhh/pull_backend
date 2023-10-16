#Librerias
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

#Serializers
from .serializers import WorkerHcmSerializer, WorkerPeopleSoftSerializer

#Odt
from . .odts import WorkerOdt

# Service
from ..services.workerServiceHcm import WorkerServiceHcm
from ..services.workerServicePeopleSoft import WorkerServicePeopleSoft


# HCM

@api_view(['GET','POST'])
def worker_hcm_api_view(request):
    if request.method == 'GET':
        worker_service = WorkerServiceHcm()
        try:
            workers = worker_service.get_workers_hcm()
            workers_serializer = WorkerHcmSerializer(workers, many=True)
            return Response(workers_serializer.data,status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def worker_hcm_detail_api_view(request,pk):
    if request.method == 'GET':
        worker_service = WorkerServiceHcm()
        try:
            worker = worker_service.get_worker_hcm(pk)
            worker_serializer = WorkerHcmSerializer(worker)
            return Response(worker_serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)

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
            # print("Entre a la excepcion de worker_update_api_view -> message: " + str(e))
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)


# PeopleSoft

@api_view(['GET'])
def worker_peoplesoft_api_view(request):
    if request.method == 'GET':
        worker_service = WorkerServicePeopleSoft()
        try:
            workers = worker_service.get_worker_peoplesoft()
            if workers:
                workers_serializer = WorkerPeopleSoftSerializer(workers, many=True)
                return Response(workers, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)