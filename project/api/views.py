from django.db.models import Q
from django.shortcuts import render

# Implement your api at here

# Create your views here.

import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from api.models import *
from api.serializers import *
from user.helper.authentication import Authentication
from user.helper.json import create_json_response
from user.models import *
from user.helper.string import *


class ProvinceInfo(APIView):
    parser_classes = (MultiPartParser,)

    """
    .../api/location
    :usage get all location
    :return Json 
    """

    def get(self, request):
        try:
            provinces = Province.objects.all()
            # user = Street.objects.filter(
            #     Q(province_id='1'),
            #     Q(district_id='1')
            # )
            serializer = ProvinceSerializer(provinces, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


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
        try:
            province = self.get_object(id)
            serializer = ProvinceSerializer(province)
            return Response(serializer.data)
        except Exception as e:
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


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
            error_header = {'error_code': EC_FAIL, 'error_message': 'not found'}
            return create_json_response(error_header, error_header, status_code=200)
            # return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, p_id, d_id):
        try:
            district = self.get_object(p_id, d_id)
            serializer = DistrictSerializer(district)
            return Response(serializer.data)
        except Exception as e:
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class EstateTypeInfo(APIView):
    parser_classes = (MultiPartParser,)

    """
    .../api/estatetype
    :usage get all estate type
    :return Json 
    """

    def get(self, request):
        try:
            estate = EstateType.objects.all()
            serializer = EstateTypeSerializer(estate, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class EstateStatusInfo(APIView):
    parser_classes = (MultiPartParser,)

    """
    .../api/estatestatus
    :usage get all estate status
    :return Json 
    """

    def get(self, request):
        try:
            estate = EstateStatus.objects.all()
            serializer = EstateStatusSerializer(estate, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class ProjectInfo(APIView):
    parser_classes = (MultiPartParser,)

    """
    .../api/project
    :usage get all project
    :return Json 
    """

    def get(self, request):
        try:
            project = Project.objects.all()
            serializer = ProjectSerializer(project, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class TransactionTypeInfo(APIView):
    parser_classes = (MultiPartParser,)

    """
    .../api/transaction
    :usage get all project
    :return Json 
    """

    def get(self, request):
        transaction_type = TransactionType.objects.all()
        serializer = TransactionTypeSerializer(transaction_type, many=True)
        return Response(serializer.data)


class PostInfo(APIView):
    parser_classes = (MultiPartParser,)

    def modify_input_for_multiple_files(self, estate_id, image):
        dict = {}
        dict['estate'] = estate_id
        dict['image'] = image
        return dict

    """
    .../api/post/
    create a post
    :require user token 
    :param:     
    :return 
    """
    def post(self, request):
        try:
            # ------------------- Authentication User ---------------------#

            error_header, status_code = Authentication().authentication(request, type_token='user')
            if error_header['error_code']:
                return create_json_response(error_header, error_header, status_code=status_code)

            # ------------------- Get Parameters ---------------------#
            user_id = error_header['id']

            json_data = request.data
            title = json_data['title']
            estateType = json_data['estateType']
            estateStatus = json_data['estateStatus']
            project = json_data['project']
            province = json_data['province']
            district = json_data['district']
            ward = json_data['ward']
            street = json_data['street']
            numberOfRoom = json_data['numberOfRoom']
            description = json_data['description']
            detail = json_data['detail']
            price = json_data['price']
            area = json_data['area']
            contact = json_data['contact']
            images = dict(json_data.lists())['image']
            transaction = json_data['transaction']

            try:
                # ------------------- Create Estate ---------------------#
                estateType_instance = EstateType.objects.get(id=estateType)
                estateStatus_instance = EstateStatus.objects.get(id=estateStatus)
                project_instance = Project.objects.get(id=project)
                province_instance = Province.objects.get(id=province)
                district_instance = District.objects.get(id=district)
                ward_instance = Ward.objects.get(id=ward)
                street_instance = Street.objects.get(id=street)
                estate = Estate(
                    title=title,
                    estateType=estateType_instance,
                    estateStatus=estateStatus_instance,
                    project=project_instance,
                    province=province_instance,
                    district=district_instance,
                    ward=ward_instance,
                    street=street_instance,
                    numberOfRoom=numberOfRoom,
                    description=description,
                    detail=detail,
                    price=price,
                    area=area,
                    contact=contact
                )
                estate.save()

                # ------------------- Create Image ---------------------#

                estate_id = estate.id
                for img_name in images:
                    modified_data = self.modify_input_for_multiple_files(estate_id, img_name)
                    file_serializer = EstateImageSetterSerializer(data=modified_data)
                    print(file_serializer)
                    if file_serializer.is_valid():
                        file_serializer.save()

                # ------------------- Create Post ---------------------#
                #
                error_header = {'error_code': EC_SUCCESS, 'error_message': EM_SUCCESS}
                return create_json_response(error_header, error_header, status_code=200)

            except EstateType.DoesNotExist:
                error_header = {'error_code': EC_FAIL, 'error_message': ' fail'}
                return create_json_response(error_header, error_header, status_code=200)

        except KeyError:
            error_header = {'error_code': EC_FAIL, 'error_message': 'Missing require fields'}
            return create_json_response(error_header, error_header, status_code=200)

        except Exception as e:
            print(e)
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class EstateInfo(APIView):
    parser_classes = (MultiPartParser,)

    """
        .../api/estate/
        return all estate
        :return 
    """
    def get(self, request):
        try:
            estate = Estate.objects.all()
            serializer = EstateSerializer(estate, context={"request": request}, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class EstateDetailInfo(APIView):
    parser_classes = (MultiPartParser,)
    """
    .../api/estate/<id>
    :return get a special estate (Json format) 
    """

    def get_object(self, id):
        try:
            return Estate.objects.get(id=id)
        except Estate.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        try:
            estate = self.get_object(id)
            serializer = EstateDetailSerializer(estate, context={"request": request})
            return Response(serializer.data)
        except Exception as e:
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)

