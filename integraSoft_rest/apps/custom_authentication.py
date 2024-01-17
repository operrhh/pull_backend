from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from django.conf import settings

class CustomTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed('Token no válido')

        if not token.user.is_active:
            raise AuthenticationFailed('El usuario asociado a este token no está activo')

        if self.token_expired(token):
            token.delete()
            raise AuthenticationFailed('Token expirado')

        return (token.user, token)

    def token_expired(self, token):
        # Comparar la fecha de expiración con la fecha y hora actuales
        expiration_time = token.created + timezone.timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS)
        return expiration_time < timezone.now()