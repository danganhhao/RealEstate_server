from django.db.models import Q
from django.shortcuts import render

# Implement your api at here

# Create your views here.

import json
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from api.models import Street
from api.serializers import StreetSerializer


class StreetInfo(APIView):
    parser_classes = (MultiPartParser,)
    """
    /user/
    Receive: 
    """

    def get(self, request):
        user = Street.objects.all()
        # user = Street.objects.filter(
        #     Q(province_id='1'),
        #     Q(district_id='1')
        # )
        # user = Street.objects.get(province_id='1')
        serializer = StreetSerializer(user, many=True)
        return Response(serializer.data)
