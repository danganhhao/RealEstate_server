import os
from random import randint
from datetime import datetime

from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings

from api.models import Post
from user.helper.authentication import Authentication
from user.helper.utils import *
from user.helper.json import *
from user.helper.token import create_token
from user.helper.email_support import reset_password_email
from user.models import *
from user.serializers import UserSerializer

import cloudinary.uploader


# Create your views here.


class UserInfo(APIView):
    parser_classes = (MultiPartParser,)
    """
    /user/
    Receive:
    """

    def get(self, request):
        try:
            user = User.objects.all()
            serializer = UserSerializer(user, context={"request": request}, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            error_header = {'error_code': EC_FAIL, 'error_message': EM_FAIL + str(e)}
            return create_json_response(error_header, error_header, status_code=200)

    """
        /user/
        Create a new user
        Receive: username & password or token
    """

    def post(self, request):

        # --------------- Check Admin Token for permission -------------

        # error_header, status_code = Authentication().authentication(request, type_token='user')
        #
        # if error_header['error_code']:
        #     return create_json_response(error_header, error_header, status_code=status_code)

        # --------------- Register Flow --------------------------------
        # json_data = json.loads(request.body.decode('utf-8'))

        try:
            json_data = request.data

            name = json_data.get('name')
            username = json_data.get('username')
            password = json_data.get('password')
            gender = json_data.get('gender')
            email = json_data.get('email')
            address = json_data.get('address', None)
            phoneNumber = json_data.get('phoneNumber', None)
            identifyNumber = json_data.get('identifyNumber', None)
            birthday = json_data.get('birthday', None)
            avatar = json_data.get('avatar', None)

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
                error_header = {'error_code': EC_EXIST, 'error_message': EM_EXIST + "username"}
                return create_json_response(error_header, error_header, status_code=200)
            elif is_email_exist(user.email):
                error_header = {'error_code': EC_EXIST, 'error_message': EM_EXIST + "email"}
                return create_json_response(error_header, error_header, status_code=200)

            if avatar:
                # ---- Check image size --------
                if not is_image_size_valid(avatar.size, IMAGE_SIZE_MAX_BYTES):
                    error_header = {'error_code': EC_IMAGE_LARGE, 'error_message': EM_IMAGE_LARGE}
                    return create_json_response(error_header, error_header, status_code=200)

                path = uploadLocationUser(username, avatar.size)
                upload_data = cloudinary.uploader.upload(avatar, public_id=path)
                user.avatar = upload_data['secure_url']

            user.save()

            error_header = {'error_code': EC_SUCCESS, 'error_message': EM_SUCCESS}
            return create_json_response(error_header, error_header, status_code=200)

        except Exception as e:
            print(e)
            error_header = {'error_code': EC_FAIL, 'error_message': EM_FAIL + str(e)}
            return create_json_response(error_header, error_header, status_code=200)

    """
        /user/
        Modify a existed user
        Receive: token
    """

    def put(self, request):
        try:
            error_header, status_code = Authentication().authentication(request, type_token='user')
            if error_header['error_code'] == 0:
                return create_json_response(error_header, error_header, status_code=status_code)

            json_data = request.data
            email = json_data.get('email', None)
            address = json_data.get('address', None)
            phoneNumber = json_data.get('phoneNumber', None)
            identifyNumber = json_data.get('identifyNumber', None)
            birthday = json_data.get('birthday', None)
            avatar = json_data.get('avatar', None)

            if birthday:
                birthday = datetime.strptime(birthday, '%d/%m/%Y')
            else:
                birthday = datetime.strptime('01/01/1900', '%d/%m/%Y')

            id = error_header['id']
            try:
                if id:
                    user = User.objects.get(id=id)
                    if email is not None:
                        user.email = email
                    if address is not None:
                        user.address = address
                    if birthday is not None:
                        user.birthday = birthday
                    if phoneNumber is not None:
                        user.phoneNumber = phoneNumber
                    if identifyNumber is not None:
                        user.identifyNumber = identifyNumber

                    if avatar:
                        if user.avatar != avatar:
                            # ---- Check image size --------
                            if not is_image_size_valid(avatar.size, IMAGE_SIZE_MAX_BYTES):
                                error_header = {'error_code': EC_IMAGE_LARGE, 'error_message': EM_IMAGE_LARGE}
                                return create_json_response(error_header, error_header, status_code=200)

                            # ---- Delete old avatar ------
                            if user.avatar:
                                temp = user.avatar.index('user/')
                                temp_url = user.avatar[temp:]
                                endIndex = temp_url.index('.')
                                public_id = temp_url[:endIndex]
                                cloudinary.uploader.destroy(public_id)

                            # ---- Create new avatar ------
                            path = uploadLocationUser(user.username, avatar.size)
                            upload_data = cloudinary.uploader.upload(avatar, public_id=path)
                            user.avatar = upload_data['secure_url']

                    user.save()

                    error_header = {'error_code': EC_SUCCESS, 'error_message': 'success'}
                    return create_json_response(error_header, error_header, status_code=200)

            except UserToken.DoesNotExist:
                error_header = {'error_code': EC_FAIL, 'error_message': 'User not exist'}
                return create_json_response(error_header, error_header, status_code=200)
        except KeyError:
            error_header = {'error_code': EC_FAIL, 'error_message': 'Missing require fields'}
            return create_json_response(error_header, error_header, status_code=200)

        except Exception as e:
            print(e)
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class Login(APIView):
    parser_classes = (MultiPartParser,)

    def get_user_data(self, request, user):
        json_response = {}
        json_response['name'] = user.name
        json_response['username'] = user.username
        json_response['gender'] = user.gender
        json_response['birthday'] = str(user.birthday)
        json_response['address'] = user.address
        json_response['avatar'] = user.avatar
        json_response['phoneNumber'] = user.phoneNumber
        json_response['email'] = user.email
        json_response['identifyNumber'] = user.identifyNumber
        json_response['isAgency'] = user.isAgency
        return json_response

    """
    user/login
    :
    :usage  API receive username, password
    :return token
    """

    def post(self, request):
        try:
            error_header, status_code = Authentication().authentication(request, type_token='user')
            print(error_header)
            if error_header['error_code'] == 0:  # Login with username and password
                json_data = request.data
                username = json_data['username']
                password = json_data['password']
                try:
                    user = User.objects.get(username=username)
                    if check_password(password, user.password):
                        UserToken.objects.filter(user=user.id).delete()  # Delete token before
                        json_response = self.get_user_data(request, user)
                        json_response['token'] = create_token(model_instance=user, model_type='user')
                        error_header = {'error_code': EC_SUCCESS, 'error_message': EM_SUCCESS}
                        return create_json_response(json_response, error_header, status_code=200)
                    else:
                        error_header = {'error_code': EC_FAIL, 'error_message': EM_FAIL + 'Login fail'}
                        return create_json_response(error_header, error_header, status_code=200)

                except User.DoesNotExist:
                    error_header = {'error_code': EC_FAIL, 'error_message': EM_FAIL + 'Login fail'}
                    return create_json_response(error_header, error_header, status_code=200)

            else:  # Login with token
                id = error_header['id']
                user = User.objects.get(id=id)
                user_token = UserToken.objects.get(user=user.id)
                if user_token.token == get_token(request):
                    json_response = self.get_user_data(request, user)
                    error_header = {'error_code': EC_SUCCESS, 'error_message': EM_SUCCESS}
                    return create_json_response(json_response, error_header, status_code=200)
                else:
                    error_header = {'error_code': EC_FAIL, 'error_message': EM_FAIL + 'Login fail'}
                    return create_json_response(error_header, error_header, status_code=200)

        except KeyError:
            error_header = {'error_code': EC_FAIL, 'error_message': EM_EXIST + 'Missing require fields'}
            return create_json_response(error_header, error_header, status_code=200)

        except Exception as e:
            print(e)
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
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
            if error_header['error_code'] == 0:
                return create_json_response(error_header, error_header, status_code=status_code)

            # token = get_token(request)
            token = error_header['token']
            id = error_header['id']
            try:
                if id:
                    UserToken.objects.filter(user=id).delete()
                    error_header = {'error_code': EC_SUCCESS, 'error_message': 'success'}
                    return create_json_response(error_header, error_header, status_code=200)

            except UserToken.DoesNotExist:
                error_header = {'error_code': EC_FAIL, 'error_message': 'Logout fail'}
                return create_json_response(error_header, error_header, status_code=200)
        except KeyError:
            error_header = {'error_code': EC_FAIL, 'error_message': 'Missing require fields'}
            return create_json_response(error_header, error_header, status_code=200)

        except Exception as e:
            print(e)
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
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
                    error_header = {'error_code': EC_SUCCESS, 'error_message': EM_SUCCESS}
                    return create_json_response(error_header, error_header, status_code=200)

            except UserToken.DoesNotExist:
                error_header = {'error_code': EC_FAIL, 'error_message': 'fail'}
                return create_json_response(error_header, error_header, status_code=200)
        except KeyError:
            error_header = {'error_code': EC_FAIL, 'error_message': 'Missing require fields'}
            return create_json_response(error_header, error_header, status_code=200)

        except Exception as e:
            print(e)
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
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
                    error_header = {'error_code': EC_SUCCESS, 'error_message': EM_SUCCESS}
                    return create_json_response(error_header, error_header, status_code=200)

            except UserToken.DoesNotExist:
                error_header = {'error_code': EC_FAIL, 'error_message': 'fail'}
                return create_json_response(error_header, error_header, status_code=200)
        except KeyError:
            error_header = {'error_code': EC_FAIL, 'error_message': 'Missing require fields'}
            return create_json_response(error_header, error_header, status_code=200)

        except Exception as e:
            print(e)
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class ChangePassword(APIView):
    parser_classes = (MultiPartParser,)
    """
    user/password
    change user password
    :require token header
    :return
    """

    def put(self, request):
        try:
            error_header, status_code = Authentication().authentication(request, type_token='user')
            if error_header['error_code'] == 0:
                return create_json_response(error_header, error_header, status_code=status_code)

            m_id = error_header['id']
            json_data = request.data
            old_password = json_data.get('oldPassword')
            new_password = json_data.get('newPassword')
            try:
                if m_id:
                    user = User.objects.get(id=m_id)
                    if check_password(old_password, user.password):
                        user.password = make_password(new_password)
                        user.save()
                        error_header = {'error_code': EC_SUCCESS, 'error_message': EM_SUCCESS}
                        return create_json_response(error_header, error_header, status_code=200)
                    else:
                        error_header = {'error_code': EC_FAIL, 'error_message': EM_FAIL + 'Old password not matched'}
                        return create_json_response(error_header, error_header, status_code=200)

            except User.DoesNotExist:
                error_header = {'error_code': EC_FAIL, 'error_message': 'Not found account'}
                return create_json_response(error_header, error_header, status_code=200)
        except KeyError:
            error_header = {'error_code': EC_FAIL, 'error_message': 'Missing require fields'}
            return create_json_response(error_header, error_header, status_code=200)

        except Exception as e:
            print(e)
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class RegisterAgency(APIView):
    parser_classes = (MultiPartParser,)

    def checkNullField(self, field):
        if field is None or field == "" or field == 'NULL':
            return True
        return False

    def returnMissFieldError(self, field):
        error_header = {'error_code': EC_MISS_REQUIRE_INFO, 'error_message': EM_FAIL + 'Miss field: ' + str(field)}
        return create_json_response(error_header, error_header, status_code=200)

    """
    user/checkingaccount/
    check user account. If approve, return info, else, return false
    :require token header
    :return
    """

    def post(self, request):
        try:
            error_header, status_code = Authentication().authentication(request, type_token='user')
            if error_header['error_code'] == 0:
                return create_json_response(error_header, error_header, status_code=status_code)

            user_id = error_header['id']
            try:
                if user_id:
                    user_instance = User.objects.get(id=user_id)
                    post_obj = Post.objects.filter(user=user_instance)
                    if post_obj.count() < MINIMUM_NUMBER_OF_POSTS_PER_AGENCY:
                        error_header = {'error_code': EC_NOT_ENOUGH_POST, 'error_message': EM_FAIL + 'The number of '
                                                                                                     'posts must be '
                                                                                                     'greater than or '
                                                                                                     'equal to 20'}
                        return create_json_response(error_header, error_header, status_code=200)

                    if self.checkNullField(user_instance.gender):
                        return self.returnMissFieldError('gender')
                    if self.checkNullField(user_instance.birthday):
                        return self.returnMissFieldError('birthday')
                    if self.checkNullField(user_instance.address):
                        return self.returnMissFieldError('address')
                    if self.checkNullField(user_instance.avatar):
                        return self.returnMissFieldError('avatar')
                    if self.checkNullField(user_instance.phoneNumber):
                        return self.returnMissFieldError('phoneNumber')
                    if self.checkNullField(user_instance.identifyNumber):
                        return self.returnMissFieldError('identifyNumber')

                    error_header = {'error_code': EC_SUCCESS, 'error_message': 'Ready to upgrade to agency account'}
                    return create_json_response(error_header, error_header, status_code=200)

                else:
                    error_header = {'error_code': EC_FAIL, 'error_message': EM_FAIL + 'User not exist'}
                    return create_json_response(error_header, error_header, status_code=200)

            except User.DoesNotExist:
                error_header = {'error_code': EC_FAIL, 'error_message': 'Not found account'}
                return create_json_response(error_header, error_header, status_code=200)
        except KeyError:
            error_header = {'error_code': EC_FAIL, 'error_message': 'Missing require fields'}
            return create_json_response(error_header, error_header, status_code=200)

        except Exception as e:
            print(e)
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class AgencyInfo(APIView):
    parser_classes = (MultiPartParser,)

    def checkNullField(self, field):
        if field is None or field == "" or field == 'NULL':
            return True
        return False

    def returnMissFieldError(self, field):
        error_header = {'error_code': EC_MISS_REQUIRE_INFO, 'error_message': EM_FAIL + 'Miss field: ' + str(field)}
        return create_json_response(error_header, error_header, status_code=200)

    """
        /user/agency/
        Upgrade normal account to agency account
        Receive: token
    """

    def post(self, request):
        try:
            error_header, status_code = Authentication().authentication(request, type_token='user')
            if error_header['error_code'] == 0:
                return create_json_response(error_header, error_header, status_code=status_code)

            user_id = error_header['id']
            try:
                if user_id:
                    user = User.objects.get(id=user_id)
                    post_obj = Post.objects.filter(user=user)
                    if post_obj.count() < MINIMUM_NUMBER_OF_POSTS_PER_AGENCY:
                        error_header = {'error_code': EC_FAIL, 'error_message': EM_FAIL + 'The number of posts must be '
                                                                                          'greater than or equal to 20'}
                        return create_json_response(error_header, error_header, status_code=200)

                    if self.checkNullField(user.gender):
                        return self.returnMissFieldError('gender')
                    if self.checkNullField(user.birthday):
                        return self.returnMissFieldError('birthday')
                    if self.checkNullField(user.address):
                        return self.returnMissFieldError('address')
                    if self.checkNullField(user.avatar):
                        return self.returnMissFieldError('avatar')
                    if self.checkNullField(user.phoneNumber):
                        return self.returnMissFieldError('phoneNumber')
                    if self.checkNullField(user.identifyNumber):
                        return self.returnMissFieldError('identifyNumber')

                    user.isAgency = True
                    user.save()

                    error_header = {'error_code': EC_SUCCESS, 'error_message': 'success'}
                    return create_json_response(error_header, error_header, status_code=200)

            except UserToken.DoesNotExist:
                error_header = {'error_code': EC_FAIL, 'error_message': 'User not exist'}
                return create_json_response(error_header, error_header, status_code=200)
        except KeyError:
            error_header = {'error_code': EC_FAIL, 'error_message': 'Missing require fields'}
            return create_json_response(error_header, error_header, status_code=200)

        except Exception as e:
            print(e)
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)
