from django.db.models import Q
from django.shortcuts import render

# Implement your api at here

# Create your views here.

import json
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from api.models import Province
from api.serializers import ProvinceSerializer


class LocationInfo(APIView):
    parser_classes = (MultiPartParser,)
    """
    """

    def get(self, request):
        user = Province.objects.all()
        # user = Street.objects.filter(
        #     Q(province_id='1'),
        #     Q(district_id='1')
        # )
        # user = Province.objects.get(id='1')
        serializer = ProvinceSerializer(user, many=True)
        return Response(serializer.data)
