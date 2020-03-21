import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from user.models import UserToken, User


class Authentication(BaseAuthentication):
    def authentication(self, request, type_token):
        try:
            auth_error = self.authenticate(request)
            if auth_error['error_code'] or auth_error['type'] not in type_token:
                error_header = auth_error
                return error_header, 200
            else:
                return auth_error, 200
        except Exception as e:
            error_header = {'error_code': 100, 'error_message': 'Something wrong! Please contact \
                                 server admin. Error: ' + str(e)}
            return error_header, 200

    @staticmethod
    def authenticate_credentials(token, request):
        """
        :return user Token
        """

        credential = {}
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            credential = {'type': payload['type'], 'error_code': 0, 'error_message': 'Success'}
            # handle token of login user
            if payload['type'] == 'user':
                user_id = payload['id']
                email = payload['email']

                user = User.objects.get(username=user_id, email=email)
                user_token = user.usertoken_set.get(token=token)

                credential['user_id'] = user.username
                credential['token'] = token
            # For admin token
            elif payload['type'] == 'admin' \
                    or payload['type'] == 'reset-password' or payload['type'] == 'forgot-password':

                return credential

        except jwt.ExpiredSignatureError or jwt.DecodeError or jwt.InvalidIssuerError as e:
            credential['error_code'] = 1
            credential['error_message'] = 'JWT Error: ' + str(e)
        except User.DoesNotExist or UserToken.DoesNotExist:
            credential['error_code'] = 1
            credential['error_message'] = 'Invalid Token'
        except Exception as e:
            credential['error_code'] = 1
            credential['error_message'] = 'Something wrong: Invalid Token - ' + str(e)

        return credential

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        error_code, error_message = 0, 'Success'
        if not auth or auth[0].lower() != b'token':
            error_code = 1
            error_message = "Authentication failed: Can't find the Authentication token."
        elif len(auth) == 1:
            error_code = 1
            error_message = "Authentication failed: Invalid token header. No credentials provided."
        elif len(auth) > 2:
            error_code = 1
            error_message = 'Authentication failed: Invalid token header.'

        if error_code:
            return dict(error_code=error_code, error_message=error_message)

        try:
            token = auth[1]
            if token != "null":
                return self.authenticate_credentials(token, request)
            else:
                error_message = 'Null token not allowed.'
        except UnicodeError:
            error_message = 'Invalid token header. Token string should not contain invalid characters.'

        return dict(error_code=1, error_message=error_message)