from ...custom_authentication import CustomTokenAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, AllowAny
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

# Decorators
from rest_framework.decorators import api_view, permission_classes, authentication_classes

# Models
from apps.users.models import User

# Serializers
from apps.users.api.serializers import UserSerializer, UserListSerializer, UserLoginSerializer


@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([AllowAny])
def user_api_view(request):
    if request.method == 'GET':
        users = User.objects.values('id','username','email','password')
        users_serializer = UserListSerializer(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_create_api_view(request):
    if request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'message':'Usuario creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAdminUser])
def user_detail_api_view(request, pk=None):
    
    user = User.objects.filter(id=pk).first()

    if user:

        if request.method == 'GET':
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            user_serializer = UserSerializer(user, data=request.data)

            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            user.delete()
            return Response({'message':'Usuario eliminado correctamente'}, status=status.HTTP_200_OK)

    return Response({'message':'No se ha encontrado un usuario con estos datos'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login_api_view(request):
    if request.method == 'POST':
        user_serializer = UserLoginSerializer(data=request.data)
        if user_serializer.is_valid():
            usr = user_serializer.validated_data['username']
            psw = user_serializer.validated_data['password']
            user = authenticate(username=usr, password=psw)
            if user:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)