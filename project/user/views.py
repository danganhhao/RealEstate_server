from django.shortcuts import render

# Create your views here.

import json

from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import *
from rest_framework import authentication, permissions, status
from rest_framework.views import APIView
from user.helper.json import *
from user.models import *
from user.serializers import UserSerializer


class UserInfo(APIView):
    def get(self, request, format=None):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
        # return Response(JSONRenderer().render(serializer.data))

    def post(self, request):
        return Response({"1231": "123123"})

# @api_view(['GET', ])
# def userinfo(request):
#     if request.method == 'GET':
#         return Response({"1231": "123123"})
