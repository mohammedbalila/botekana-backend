from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class CustomJWTAuthentication(JSONWebTokenAuthentication):
    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id.
        """
        pk = payload.get('user_id')

        if not pk:
            raise exceptions.AuthenticationFailed("Invalid Payload.")

        try:
            user = get_user_model().objects.get(pk=pk)
        except:
            raise exceptions.AuthenticationFailed("Invalid Signature.")

        return user
