from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth import get_user_model
import jwt

class JWTAuthenticationFromCookie(BaseAuthentication):
    def authenticate(self, request):
        # Get the token from the cookies
        token = request.COOKIES.get('access_token')
        if not token:
            return None  # Return None if there's no token, allowing other authentication methods

        try:
            # Decode the token using the secret key
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token.')

        # Fetch the user based on the ID stored in the payload
        user_model = get_user_model()
        try:
            user = user_model.objects.get(id=payload['user_id'])
        except user_model.DoesNotExist:
            raise AuthenticationFailed('User not found.')

        # Return the user and None (no token object needed here)
        return (user, None)
