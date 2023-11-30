from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from apps.users.models import User
from rest_framework import status
from django.test import TestCase

# Create your tests here.

class UserTestCase(TestCase):
    # Configura datos iniciales para las pruebas
    def setUp(self):
        self.userAdmin = User.objects.create(
            username = 'testuser',
            email = 'testuser@gmail.com',
            name = 'testname',
            last_name = 'testlastname',
            password = 'test123',
            is_staff = True,
            is_superuser = True
        )
        self.token = Token.objects.create(user=self.userAdmin)
        self.api_client = APIClient()

    def test_user_api_view_get(self):
        # Prueba para GET en user_api_view
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.api_client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)