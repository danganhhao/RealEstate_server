from django.db.models import Q
from django.shortcuts import render

# Implement your api at here

# Create your views here.

import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from api.models import Province, District
from api.serializers import ProvinceSerializer, DistrictSerializer
from user.helper.json import create_json_response


class ProvinceInfo(APIView):
    parser_classes = (MultiPartParser,)

    """
    .../api/location
    :usage get all location
    :return Json 
    """

    def get(self, request):
        provinces = Province.objects.all()
        # user = Street.objects.filter(
        #     Q(province_id='1'),
        #     Q(district_id='1')
        # )
        serializer = ProvinceSerializer(provinces, many=True)
        return Response(serializer.data)


class ProvinceDetailInfo(APIView):
    parser_classes = (MultiPartParser,)
    """
    .../api/province/<id>
    :return get a special province (Json format) 
    """

    def get_object(self, id):
        try:
            return Province.objects.get(id=id)
        except Province.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        province = self.get_object(id)
        serializer = ProvinceSerializer(province)
        return Response(serializer.data)


class DistrictDetailInfo(APIView):
    parser_classes = (MultiPartParser,)
    """
    .../api/province/<p_id>/district/<d_id>
    :return get a special district of a special province (Json format) 
    """

    def get_object(self, p_id, d_id):
        try:
            return District.objects.get(id=d_id, province_id=p_id)
        except District.DoesNotExist:
            error_header = {'error_code': 0, 'error_message': 'not found'}
            return create_json_response(error_header, error_header, status_code=200)
            # return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, p_id, d_id):
        district = self.get_object(p_id, d_id)
        serializer = DistrictSerializer(district)
        return Response(serializer.data)
