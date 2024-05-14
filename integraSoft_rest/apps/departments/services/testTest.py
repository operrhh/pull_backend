import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse


class TestService:
    def get_test(self):
        # Realizar una solicitud a la página original
        url_original = 'https://www.paginaoriginal.com'
        response = requests.get(url_original)