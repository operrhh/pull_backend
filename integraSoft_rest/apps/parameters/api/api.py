from rest_framework.response import Response
from rest_framework import status

# Decorators
from rest_framework.decorators import api_view

# Models
from apps.parameters.models import Parameter, ParameterType

# Serializers
from apps.parameters.api.serializers import ParameterSerializer, ParameterTypeSerializer


@api_view(['GET','POST'])
def parameter_api_view(request):

    if request.method == 'GET':
        parameters = Parameter.objects.all()
        parameters_serializer = ParameterSerializer(parameters, many=True)
        return Response(parameters_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        parameter_serializer = ParameterSerializer(data=request.data)

        if parameter_serializer.is_valid():
            parameter_serializer.save()
            return Response({'message':'Parámetro creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(parameter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def parameter_detail_api_view(request, pk=None):
    
    parameter = Parameter.objects.filter(id=pk).first()

    if parameter:

        if request.method == 'GET':
            parameter_serializer = ParameterSerializer(parameter)
            return Response(parameter_serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            parameter_serializer = ParameterSerializer(parameter, data=request.data)

            if parameter_serializer.is_valid():
                parameter_serializer.save()
                return Response(parameter_serializer.data, status=status.HTTP_200_OK)
            return Response(parameter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            parameter.delete()
            return Response({'message':'Parámetro eliminado correctamente'}, status=status.HTTP_200_OK)

    return Response({'message':'No se ha encontrado un parámetro con estos datos'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def parameterType_api_view(request):

    if request.method == 'GET':
        parameterTypes = ParameterType.objects.all()
        parameterTypes_serializer = ParameterTypeSerializer(parameterTypes, many=True)
        return Response(parameterTypes_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        parameterType_serializer = ParameterTypeSerializer(data=request.data)

        if parameterType_serializer.is_valid():
            parameterType_serializer.save()
            return Response({'message':'Tipo de parámetro creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(parameterType_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def parameterType_detail_api_view(request, pk=None):
    
    parameterType = ParameterType.objects.filter(id=pk).first()

    if parameterType:

        if request.method == 'GET':
            parameterType_serializer = ParameterTypeSerializer(parameterType)
            return Response(parameterType_serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            parameterType_serializer = ParameterTypeSerializer(parameterType, data=request.data)

            if parameterType_serializer.is_valid():
                parameterType_serializer.save()
                return Response(parameterType_serializer.data, status=status.HTTP_200_OK)
            return Response(parameterType_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            parameterType.delete()
            return Response({'message':'Tipo de parámetro eliminado correctamente'}, status=status.HTTP_200_OK)

    return Response({'message':'No se ha encontrado un tipo de parámetro con estos datos'}, status=status.HTTP_400_BAD_REQUEST)