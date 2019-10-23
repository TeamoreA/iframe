import jwt
import datetime
from rest_framework.authentication import TokenAuthentication
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model


class JWTAuthentication(TokenAuthentication):
    keyword = 'Bearer'

    @staticmethod
    def generate_token(userdata):
        """
        generate JWT token from userdata
        """
        secret = settings.SECRET_KEY
        token = jwt.encode({
            'userdata': userdata,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=2)
        }, secret)
        # return UTF-8 token
        return token.decode('utf-8')

    @staticmethod
    def decode_token(token):
        """
        decode JWT token
        """
        user_details = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms='HS256'
        )
        return user_details

    def authenticate_credentials(self, key):
        try:
            payload = jwt.decode(key, settings.SECRET_KEY)
            username = payload['userdata']['username']
            user = get_user_model().objects.get(username=username)
        except (jwt.DecodeError, get_user_model().DoesNotExist):
            raise AuthenticationFailed('Invalid token')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        return user, payload


# class GenerateApiToken():
#     """class to generate the API token that doesn't expire"""
secret_key = settings.SECRET_KEY + "_api_token"


def generate_api_token(userdata):
    """
    generate JWT token from user_data
    """
    token = jwt.encode({
        'userdata': userdata,
        'iat': datetime.datetime.utcnow()
    }, secret_key)
    # return UTF-8 token
    return token.decode('utf-8')


def authenticate_credentials(api_token):
    try:
        payload = jwt.decode(api_token, secret_key)
        id = payload['userdata']['id']
        user = get_user_model().objects.get(pk=id)
    except (jwt.DecodeError, get_user_model().DoesNotExist):
        raise AuthenticationFailed('Invalid api token')
    return user
