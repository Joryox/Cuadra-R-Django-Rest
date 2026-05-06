from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.utils.translation import gettext_lazy as _
from api.models import Usuario

class CuadraJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication backend for Cuadra Erre.
    Since we use a custom 'Usuario' model that does not inherit from AbstractUser,
    the default JWTAuthentication crashes trying to find the UUID in auth.User.
    This overrides get_user to specifically query our api.Usuario model.
    """
    def get_user(self, validated_token):
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(_("Token contained no recognizable user identification"))

        try:
            user = Usuario.objects.get(id=user_id)
        except Usuario.DoesNotExist:
            raise AuthenticationFailed(_("User not found"), code="user_not_found")

        if not user.activo:
            raise AuthenticationFailed(_("User is inactive"), code="user_inactive")

        return user
