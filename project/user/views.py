import os
from random import randint
from datetime import datetime

from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response


from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings

from user.helper.authentication import Authentication
from user.helper.utils import is_username_exist, is_email_exist, is_image_size_valid, is_image_aspect_ratio_valid
from user.helper.json import *
from user.helper.token import create_token
from user.helper.email_support import reset_password_email
from user.helper.utils import get_token
from user.models import *
from user.serializers import UserSerializer


# Create your views here.

IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 2  # 2MB


class UserInfo(APIView):
    parser_classes = (MultiPartParser,)
    """
    /user/
    Receive: 
    """

    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, context={"request": request}, many=True)
        return Response(serializer.data)

    def post(self, request):

        # --------------- Check Admin Token for permission -------------

        # error_header, status_code = Authentication().authentication(request, type_token='user')
        #
        # if error_header['error_code']:
        #     return create_json_response(error_header, error_header, status_code=status_code)

        # --------------- Register Flow --------------------------------
        # json_data = json.loads(request.body.decode('utf-8'))
        json_data = request.data

        name = json_data['name']
        username = json_data['username']
        password = json_data['password']
        gender = json_data['gender']
        email = json_data['email']
        address = json_data['address']
        phoneNumber = json_data['phoneNumber']
        identifyNumber = json_data['identifyNumber']
        birthday = json_data['birthday']
        avatar = json_data['avatar']

        try:
            if birthday:
                birthday = datetime.strptime(birthday, '%d/%m/%Y')
            else:
                birthday = datetime.strptime('01/01/1900', '%d/%m/%Y')

            user = User(
                name=name,
                username=username,
                password=make_password(password),
                gender=gender,
                email=email,
                birthday=birthday,
                address=address,
                avatar=avatar,
                phoneNumber=phoneNumber,
                identifyNumber=identifyNumber,
                pin=randint(100000, 999999)
            )

            if is_username_exist(user.username):
                error_header = {'error_code': EC_USERNAME_EXIST, 'error_message': EM_USERNAME_EXIST}
                return create_json_response(error_header, error_header, status_code=200)
            elif is_email_exist(user.email):
                error_header = {'error_code': EC_EMAIL_EXIST, 'error_message': EM_EMAIL_EXIST}
                return create_json_response(error_header, error_header, status_code=200)

            if avatar:
                url = os.path.join(settings.MEDIA_ROOT, str(avatar))
                storage = FileSystemStorage(location=url)

                with storage.open('', 'wb+') as destination:
                    for chunk in avatar.chunks():
                        destination.write(chunk)
                    destination.close()

                # Check image size
                if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
                    os.remove(url)
                    error_header = {'error_code': EC_IMAGE_LARGE, 'error_message': EM_IMAGE_LARGE}
                    return create_json_response(error_header, error_header, status_code=200)

                # Check image aspect ratio
                if not is_image_aspect_ratio_valid(url):
                    os.remove(url)
                    error_header = {'error_code': EC_IMAGE_RATIO, 'error_message': EM_IMAGE_RATIO}
                    return create_json_response(error_header, error_header, status_code=200)
                os.remove(url)

            user.save()

            error_header = {'error_code': EC_SUCCESS, 'error_message': EM_SUCCESS}
            return create_json_response(error_header, error_header, status_code=200)

        except Exception as e:
            print(e)
            error_header = {'error_code': EC_FAIL, 'error_message': EM_FAIL + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class Login(APIView):
    parser_classes = (MultiPartParser,)
    """
    user/login
    :require token header
    :usage  API receive username, password
    :return token
    """

    def post(self, request):
        ## Check permission
        try:
            json_data = request.data
            username = json_data['username']
            password = json_data['password']

            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password):
                    json_response = create_token(model_instance=user, model_type='user')
                    json_response['username'] = user.username

                    error_header = {'error_code': 0, 'error_message': 'success'}
                    return create_json_response(json_response, error_header, status_code=200)

                else:
                    error_header = {'error_code': 11, 'error_message': 'Login fail'}
                    return create_json_response(error_header, error_header, status_code=200)

            except User.DoesNotExist:
                error_header = {'error_code': 11, 'error_message': 'Login fail'}
                return create_json_response(error_header, error_header, status_code=200)
        except KeyError:
            error_header = {'error_code': 11, 'error_message': 'Missing require fields'}
            return create_json_response(error_header, error_header, status_code=200)

        except Exception as e:
            print(e)
            error_header = {'error_code': 100, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class Logout(APIView):
    parser_classes = (MultiPartParser,)
    """
    user/logout
    :require token header
    :usage  API receive username, password
    :return 
    """

    def post(self, request):
        try:
            error_header, status_code = Authentication().authentication(request, type_token='user')
            if error_header['error_code']:
                return create_json_response(error_header, error_header, status_code=status_code)

            # token = get_token(request)
            token = error_header['token']
            id = error_header['id']
            print(id)
            try:
                if id:
                    UserToken.objects.filter(user=id).delete()
                    error_header = {'error_code': 0, 'error_message': 'success'}
                    return create_json_response(error_header, error_header, status_code=200)

            except UserToken.DoesNotExist:
                error_header = {'error_code': 11, 'error_message': 'Logout fail'}
                return create_json_response(error_header, error_header, status_code=200)
        except KeyError:
            error_header = {'error_code': 11, 'error_message': 'Missing require fields'}
            return create_json_response(error_header, error_header, status_code=200)

        except Exception as e:
            print(e)
            error_header = {'error_code': 100, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class ForgotPassword(APIView):
    parser_classes = (MultiPartParser,)
    """
    user/forgot
    :usage  API receive email
    :return send a PIN code to user email address
    """

    def post(self, request):
        try:
            data = request.data
            email = data['email']
            try:
                user = User.objects.get(email=email)
                if user.email != "":
                    reset_password_email(user)
                    error_header = {'error_code': 0, 'error_message': 'success'}
                    return create_json_response(error_header, error_header, status_code=200)

            except UserToken.DoesNotExist:
                error_header = {'error_code': 11, 'error_message': 'fail'}
                return create_json_response(error_header, error_header, status_code=200)
        except KeyError:
            error_header = {'error_code': 11, 'error_message': 'Missing require fields'}
            return create_json_response(error_header, error_header, status_code=200)

        except Exception as e:
            print(e)
            error_header = {'error_code': 100, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class ResetPassword(APIView):
    parser_classes = (MultiPartParser,)
    """
    user/reset
    :usage  API receive pin, new password
    :return status success or failed
    """

    def post(self, request):
        try:
            data = request.data
            pin = data['pin']
            password = data['password']
            try:
                user = User.objects.get(pin=pin)
                if user.pin != "":
                    user.password = make_password(password)
                    user.pin = randint(100000, 999999)
                    user.save()
                    error_header = {'error_code': 0, 'error_message': 'success'}
                    return create_json_response(error_header, error_header, status_code=200)

            except UserToken.DoesNotExist:
                error_header = {'error_code': 11, 'error_message': 'fail'}
                return create_json_response(error_header, error_header, status_code=200)
        except KeyError:
            error_header = {'error_code': 11, 'error_message': 'Missing require fields'}
            return create_json_response(error_header, error_header, status_code=200)

        except Exception as e:
            print(e)
            error_header = {'error_code': 100, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)

