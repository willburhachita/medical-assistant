import time

import jwt
from rest_framework.permissions import IsAuthenticated, AllowAny

from common.utils import CipherUtils
from environment.main import JWT_ALGORITHM, JWT_SECRET_KEY
from environment.variables import EnvironmentVariable
from exceptions import TokenExpired, UnauthorizedAccess, ClientSignatureExpired, UnauthorizedClient
from user.models import User


class IsValidated(AllowAny):
    # Validator class for JWT Access Token

    def has_permission(self, request, view):
        """
        Access Token Validation using JWT
        It parses the token using the secret key
        if it's a valid token will allow to access the apis or returns UnAuthorizedAccess (401)

        :param request: Http Request (Should contain HTTP_AUTHORIZATION header)
        :param view: Respective View that has been called
        :return: True if valid user
        """
        try:
            auth_token = request.META.get('HTTP_AUTHORIZATION', ' ')
            token = auth_token.split(' ')
            payload = jwt.decode(token[1], JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            request.user = User.objects.get(pk=payload.get("user_id"), is_active=True)
            request.is_authenticated = True
            return True
        except User.DoesNotExist:
            raise UnauthorizedAccess()
        except jwt.exceptions.DecodeError:
            raise UnauthorizedAccess('Invalid Access Token')
        except jwt.exceptions.ExpiredSignatureError:
            raise TokenExpired()


class IsSuperUser(IsValidated):
    # Validated whether the user is Super User

    def has_permission(self, request, view):
        is_valid = super(IsSuperUser, self).has_permission(request, view)
        if is_valid and request.user.is_superuser:
            return True
        raise UnauthorizedAccess('Only superuser can access')


class ValidClient(AllowAny):

    def has_permission(self, request, view):
        """
        Decrypts the X-API-KEY (AES Cipher text) and compares with the Client ID
        to verify the API Client (Or) Checks the X-API-KEY with the Open API Key to verify Request
        @param request: Django Request
        @param view: API View Class
        @return: True or Raise Unauthorized Access
        """
        api_key = request.headers.get('X-Api-Key', '')
        if api_key == EnvironmentVariable.API_DEV_SECRET_KEY:
            # Only use API_DEV_SECRET_KEY from the local
            # Don't add in Deployment
            return True
        try:
            decrypted_string = CipherUtils.decrypt(api_key)
            client_id, timestamp = decrypted_string.split(':', 1)
            current_timestamp = int(time.time())
            if client_id == EnvironmentVariable.CLIENT_ID:
                if not current_timestamp - 30 < int(timestamp) < current_timestamp + 30:
                    raise ClientSignatureExpired()
                return True
            raise UnauthorizedClient()
        except ValueError:
            raise UnauthorizedClient()


class OnlySuperUser(IsAuthenticated):
    def has_permission(self, request, view):
        if super(OnlySuperUser, self).has_permission(request, view) and request.user.is_superuser:
            return True
        raise UnauthorizedAccess('Only superuser can access')
