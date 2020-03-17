from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from user.helper.authentication import Authentication
from user.helper.check_info import is_username_exist, is_email_exist
from django.contrib.auth.hashers import make_password, check_password
from user.helper.json import *
from user.models import *


# Create your views here.
from user.serializers import UserSerializer


class UserInfo(APIView):

    parser_classes = (MultiPartParser, )
    """
    user/register
    Receive:
    """
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request):

        # --------------- Check Admin Token for permission -------------

        error_header, status_code = Authentication().authentication(request, type_token='admin')

        if error_header['error_code']:
            return create_json_response(error_header, error_header, status_code=status_code)

        # --------------- Register Flow --------------------------------
        # json_data = json.loads(request.body.decode('utf-8'))
        json_data = request.data

        name = json_data['name']
        username = json_data['username']
        password = json_data['password']
        gender = json_data['gender']
        email = json_data['email']
        birthday = datetime.strptime(json_data['birthday'], '%d/%m/%Y')
        address = json_data['address']
        # avatar = json_data['avatar']
        phoneNumber = json_data['phoneNumber']
        identifyNumber = json_data['identifyNumber']

        try:

            user = User(
                name=name,
                username=username,
                password=make_password(password),
                gender=gender,
                email=email,
                birthday=birthday,
                address=address,
                # avatar=avatar,
                phoneNumber=phoneNumber,
                identifyNumber=identifyNumber,
            )

            if is_username_exist(user.username):
                error_header = {'error_code': 2, 'error_message': 'username existed'}
                return create_json_response(error_header, error_header, status_code=200)
            elif is_email_exist(user.email):
                error_header = {'error_code': 3, 'error_message': 'email existed'}
                return create_json_response(error_header, error_header, status_code=200)

            user.save()

            error_header = {'error_code': 0, 'error_message': 'success'}
            return create_json_response(error_header, error_header, status_code=200)

        except Exception as e:
            print(e)
            error_header = {'error_code': 100, 'error_message': 'Something went wrong - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)
