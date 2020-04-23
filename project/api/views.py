from django.db.models import Q
from django.shortcuts import render

# Implement your api at here

# Create your views here.

import cloudinary.uploader

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from api.models import *
from api.serializers import *
from user.helper.authentication import Authentication
from user.helper.json import create_json_response
from user.helper.utils import *
from user.models import *
from user.helper.string import *

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils import timezone


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


# ---- Block get special location with condition ----------
class ProvinceSpecialInfo(APIView):
    parser_classes = (MultiPartParser,)

    """
    .../api/s/province
    :usage get all province, it only contains (id, name, code)
    :return Json
    """

    def get(self, request):
        try:
            provinces = Province.objects.all()
            serializer = ProvinceSpecialSerializer(provinces, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class DistrictSpecialInfo(APIView):
    parser_classes = (MultiPartParser,)

    """
    .../api/s/district/<province_id>
    :param province_id
    :usage get all district of province_id, it only contains (id, name, prefix)
    :return Json
    """

    def get(self, request, id):
        try:
            districts = District.objects.filter(province_id=id)
            serializer = DistrictSpecialSerializer(districts, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class WardSpecialInfo(APIView):
    parser_classes = (MultiPartParser,)

    """
    .../api/s/ward/<district_id>
    :param district_id
    :usage get all ward of district_id, it only contains (id, name, prefix)
    :return Json
    """

    def get(self, request, id):
        try:
            wards = Ward.objects.filter(district_id=id)
            serializer = WardSerializer(wards, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class StreetSpecialInfo(APIView):
    parser_classes = (MultiPartParser,)

    """
    .../api/s/street/<district_id>
    :param district_id
    :usage get all street of district_id, it only contains (id, name, prefix)
    :return Json
    """

    def get(self, request, id):
        try:
            streets = Street.objects.filter(district_id=id)
            serializer = StreetSerializer(streets, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class ProjectSpecialInfo(APIView):
    parser_classes = (MultiPartParser,)

    """
    .../api/s/project/<district_id>
    :param district_id
    :usage get all project of district_id, it only contains (id, name, lat, lng)
    :return Json
    """

    def get(self, request, id):
        try:
            projects = Project.objects.filter(district_id=id)
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)

# ---- End block-------------------------------------------


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
    get all posts of current user
    :require user token
    :param:
    :return
    """
    def get(self, request):
        try:
            # ------------------- Authentication User ---------------------#

            error_header, status_code = Authentication().authentication(request, type_token='user')
            if error_header['error_code'] == 0:  # get posts with id
                json_data = request.data
                user_id = json_data.get('id')  # required
                page = request.GET.get('page', 1)
                try:
                    user_instance = User.objects.get(id=user_id)
                    post_obj = Post.objects.filter(user=user_instance)
                    paginator = Paginator(post_obj, ITEMS_PER_PAGE, allow_empty_first_page=True)
                    try:
                        post_sub_obj = paginator.page(page)
                        serializer = PostSerializer(post_sub_obj, context={"request": request}, many=True)
                        result = {}
                        result['current_page'] = str(page)
                        result['total_page'] = str(paginator.num_pages)
                        result['result'] = serializer.data
                        return Response(result)
                    except EmptyPage:
                        error_header = {'error_code': EC_FAIL, 'error_message': 'fail - index out of range'}
                        return create_json_response(error_header, error_header, status_code=200)

                except EstateType.DoesNotExist:
                    error_header = {'error_code': EC_FAIL, 'error_message': 'User not exist'}
                    return create_json_response(error_header, error_header, status_code=200)

            else:  # get posts with token
                user_id = error_header['id']
                page = request.GET.get('page', 1)
                try:
                    user_instance = User.objects.get(id=user_id)
                    post_obj = Post.objects.filter(user=user_instance)
                    paginator = Paginator(post_obj, ITEMS_PER_PAGE, allow_empty_first_page=True)
                    try:
                        post_sub_obj = paginator.page(page)
                        serializer = PostSerializer(post_sub_obj, context={"request": request}, many=True)
                        result = {}
                        result['current_page'] = str(page)
                        result['total_page'] = str(paginator.num_pages)
                        result['result'] = serializer.data
                        return Response(result)
                    except EmptyPage:
                        error_header = {'error_code': EC_FAIL, 'error_message': 'fail - index out of range'}
                        return create_json_response(error_header, error_header, status_code=200)

                except User.DoesNotExist:
                    error_header = {'error_code': EC_FAIL, 'error_message': 'User not exist'}
                    return create_json_response(error_header, error_header, status_code=200)

        except KeyError:
            error_header = {'error_code': EC_FAIL, 'error_message': 'Missing require fields'}
            return create_json_response(error_header, error_header, status_code=200)

        except Exception as e:
            print(e)
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)

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
            if error_header['error_code'] == 0:
                return create_json_response(error_header, error_header, status_code=status_code)

            # ------------------- Get Parameters ---------------------#
            user_id = error_header['id']

            json_data = request.data
            title = json_data.get('title')  # required
            estateType = json_data.get('estateType')  # required
            expire_after = json_data.get('expireAfter')  # required
            # estateStatus = json_data.get('estateStatus')  # required
            project = json_data.get('project', None)
            province = json_data.get('province')  # required
            district = json_data.get('district')  # required
            ward = json_data.get('ward', None)
            street = json_data.get('street', None)
            address_detail = json_data.get('addressDetail', "")
            numberOfRoom = json_data.get('numberOfRoom', "")
            description = json_data.get('description')  # required
            detail = json_data.get('detail')
            price = json_data.get('price', "")
            area = json_data.get('area', "")
            contact = json_data.get('contact', "")
            images = dict(json_data.lists()).get('image', [])
            transaction = json_data.get('transaction')  # required
            lat = json_data.get('lat', "")
            lng = json_data.get('lng', "")

            try:
                # ------------------- Create Estate ---------------------#

                # ------------------- Normalizer data -------------------#
                project_instance = None
                ward_instance = None
                street_instance = None
                estateType_instance = EstateType.objects.get(id=estateType)
                estateStatus_instance = EstateStatus.objects.get(id=10)
                province_instance = Province.objects.get(id=province)
                district_instance = District.objects.get(id=district)
                expireDays = int(expire_after)
                if project:
                    project_instance = Project.objects.get(id=project)
                if ward:
                    ward_instance = Ward.objects.get(id=ward)
                if street:
                    street_instance = Street.objects.get(id=street)
                if numberOfRoom == "":
                    numberOfRoom = 0
                if price == "":
                    price = 0
                if area == "":
                    area = 0
                if expireDays > 90:
                    expireDays = 90

                # ------------------------------------------------#
                estate = Estate(
                    title=title,
                    estateType=estateType_instance,
                    estateStatus=estateStatus_instance,
                    project=project_instance,
                    province=province_instance,
                    district=district_instance,
                    ward=ward_instance,
                    addressDetail=address_detail,
                    street=street_instance,
                    numberOfRoom=numberOfRoom,
                    description=description,
                    detail=detail,
                    price=price,
                    area=area,
                    contact=contact,
                    created_day=timezone.now(),
                    lat=lat,
                    lng=lng
                )
                estate.save()

                # ------------------- Create Image ---------------------#

                estate_id = estate.id
                for img_name in images:
                    # ---- Check image size --------
                    if img_name:
                        if not is_image_size_valid(img_name.size, IMAGE_SIZE_MAX_BYTES):
                            error_header = {'error_code': EC_IMAGE_LARGE, 'error_message': EM_IMAGE_LARGE}
                            return create_json_response(error_header, error_header, status_code=200)

                        path = uploadLocationEstate(estate_id, img_name.size)
                        upload_data = cloudinary.uploader.upload(img_name, public_id=path)
                        estate_image = EstateImage(
                            estate=estate,
                            image=upload_data['secure_url']
                        )
                        estate_image.save()

                # ------------------- Create Post ---------------------#
                user_instance = User.objects.get(id=user_id)
                transaction_instance = TransactionType.objects.get(id=transaction)
                new_post = Post(
                    user=user_instance,
                    estate=estate,
                    transaction=transaction_instance,
                    dateFrom=timezone.now(),
                    dateTo=(timezone.now() + timezone.timedelta(days=expireDays))
                )
                new_post.save()

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

    """
    .../api/post/
    modify a post
    :require user token
    :return
    """

    def put(self, request):
        try:
            # ------------------- Authentication User ---------------------#

            error_header, status_code = Authentication().authentication(request, type_token='user')
            if error_header['error_code'] == 0:
                return create_json_response(error_header, error_header, status_code=status_code)

            # ------------------- Get Parameters ---------------------#
            user_id = error_header['id']

            json_data = request.data
            estate_id = json_data.get('id')  # require
            title = json_data.get('title', None)
            estateType = json_data.get('estateType', None)
            expire_after = json_data.get('expireAfter', None)
            project = json_data.get('project', None)
            province = json_data.get('province', None)
            district = json_data.get('district', None)
            ward = json_data.get('ward', None)
            street = json_data.get('street', None)
            address_detail = json_data.get('addressDetail', None)
            numberOfRoom = json_data.get('numberOfRoom', None)
            description = json_data.get('description', None)
            detail = json_data.get('detail', None)
            price = json_data.get('price', None)
            area = json_data.get('area', None)
            contact = json_data.get('contact', None)
            new_images = dict(json_data.lists()).get('newImage', [])
            old_images = dict(json_data.lists()).get('oldImage', [])
            transaction = json_data.get('transaction', None)
            lat = json_data.get('lat', None)
            lng = json_data.get('lng', None)

            try:
                # ------------------- Modify Estate ---------------------#
                estate = Estate.objects.get(id=estate_id)
                if estate:
                    if title is not None:
                        estate.title = title
                    if estateType is not None:
                        estateType_instance = EstateType.objects.get(id=estateType)
                        estate.estateType = estateType_instance
                    if project is not None:
                        project_instance = Project.objects.get(id=project)
                        estate.project = project_instance
                    if province is not None:
                        province_instance = Province.objects.get(id=province)
                        estate.province = province_instance
                    if district is not None:
                        district_instance = District.objects.get(id=district)
                        estate.district = district_instance
                    if ward is not None:
                        ward_instance = Ward.objects.get(id=ward)
                        estate.ward = ward_instance
                    if street is not None:
                        street_instance = Street.objects.get(id=street)
                        estate.street = street_instance
                    if address_detail is not None:
                        estate.addressDetail = address_detail
                    if numberOfRoom is not None:
                        estate.numberOfRoom = numberOfRoom
                    if description is not None:
                        estate.description = description
                    if detail is not None:
                        estate.detail = detail
                    if price is not None:
                        estate.price = price
                    if area is not None:
                        estate.area = area
                    if contact is not None:
                        estate.contact = contact
                    if lat is not None:
                        estate.lat = lat
                    if lng is not None:
                        estate.lng = lng

                    # ------------------- Modify Image ---------------------#
                    # ------------------- Delete Old Image ---------------------#
                    for img_id in old_images:
                        if img_id:
                            img_obj = EstateImage.objects.get(id=img_id)
                            url = img_obj.image
                            temp = url.index('/estate/')
                            temp_url = url[temp:]
                            endIndex = temp_url.index('.')
                            public_id = temp_url[1:endIndex]
                            cloudinary.uploader.destroy(public_id)
                            img_obj.delete()

                    # ------------------- Add New Image ---------------------#
                    estate_id = estate.id
                    for img_name in new_images:
                        # ---- Check image size --------
                        if img_name:
                            if not is_image_size_valid(img_name.size, IMAGE_SIZE_MAX_BYTES):
                                error_header = {'error_code': EC_IMAGE_LARGE, 'error_message': EM_IMAGE_LARGE}
                                return create_json_response(error_header, error_header, status_code=200)

                            path = uploadLocationEstate(estate_id, img_name.size)
                            upload_data = cloudinary.uploader.upload(img_name, public_id=path)
                            estate_image = EstateImage(
                                estate=estate,
                                image=upload_data['secure_url']
                            )
                            estate_image.save()

                    # ------------------------------------------------#
                    # ------------------- Modify Post ---------------------#
                    # user_instance = User.objects.get(id=user_id)
                    post_obj = Post.objects.get(estate=estate)
                    if transaction is not None:
                        transaction_instance = TransactionType.objects.get(id=transaction)
                        post_obj.transaction = transaction_instance
                    if expire_after is not None:
                        expireDays = int(expire_after)
                        if expireDays > 90:
                            expireDays = 90
                        post_obj.dateTo = (post_obj.dateFrom + timezone.timedelta(days=expireDays))
                    post_obj.save()
                    estate.save()
                    error_header = {'error_code': EC_SUCCESS, 'error_message': EM_SUCCESS}
                    return create_json_response(error_header, error_header, status_code=200)
            except Estate.DoesNotExist:
                error_header = {'error_code': EC_FAIL, 'error_message': 'Estate not exist'}
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
            page = request.GET.get('page', 1)
            estate = Estate.objects.all().order_by('-id')
            paginator = Paginator(estate, ITEMS_PER_PAGE, allow_empty_first_page=True)
            try:
                estate_obj = paginator.page(page)
                serializer = EstateSerializer(estate_obj, context={"request": request}, many=True)
                result = {}
                result['current_page'] = page
                result['total_page'] = str(paginator.num_pages)
                result['result'] = serializer.data
                return Response(result)
            except EmptyPage:
                error_header = {'error_code': EC_FAIL, 'error_message': 'fail - index out of range'}
                return create_json_response(error_header, error_header, status_code=200)
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


class PostDetailInfo(APIView):
    parser_classes = (MultiPartParser,)
    """
    .../api/estate/<id>
    :return get a special estate (Json format)
    """

    def get_object(self, id):
        try:
            estate = Estate.objects.get(id=id)
            return Post.objects.get(estate=estate)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        try:
            estate = self.get_object(id)
            serializer = PostDetailSerializer(estate, context={"request": request})
            return Response(serializer.data)
        except Exception as e:
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class SortTypeInfo(APIView):
    parser_classes = (MultiPartParser,)

    """
    .../api/sorttype
    :usage get all sort type
    :return Json
    """

    def get(self, request):
        try:
            sort_type = SortType.objects.all()
            serializer = SortTypeSerializer(sort_type, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class FilterMaxPriceInfo(APIView):
    parser_classes = (MultiPartParser,)

    """
    .../api/filtermaxprice
    :usage get all filter max price type
    :return Json
    """

    def get(self, request):
        try:
            filter_type = FilterMaxPrice.objects.all()
            serializer = FilterMaxPriceSerializer(filter_type, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class FilterMinPriceInfo(APIView):
    parser_classes = (MultiPartParser,)

    """
    .../api/filterminprice
    :usage get all filter min price type
    :return Json
    """

    def get(self, request):
        try:
            filter_type = FilterMinPrice.objects.all()
            serializer = FilterMinPriceSerializer(filter_type, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class FilterAreaInfo(APIView):
    parser_classes = (MultiPartParser,)

    """
    .../api/filterarea
    :usage get all filter area type
    :return Json
    """

    def get(self, request):
        try:
            filter_type = FilterArea.objects.all()
            serializer = FilterAreaSerializer(filter_type, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class FilterNumberOfRoomInfo(APIView):
    parser_classes = (MultiPartParser,)

    """
    .../api/filternumberofroom
    :usage get all filter number of room type
    :return Json
    """

    def get(self, request):
        try:
            filter_type = FilterNumberOfRoom.objects.all()
            serializer = FilterNumberOfRoomSerializer(filter_type, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class FilterPostTimeInfo(APIView):
    parser_classes = (MultiPartParser,)

    """
    .../api/filterposttime
    :usage get all filter post time type
    :return Json
    """

    def get(self, request):
        try:
            filter_type = FilterPostTime.objects.all()
            serializer = FilterPostTimeSerializer(filter_type, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class SearchEngine(APIView):
    parser_classes = (MultiPartParser,)

    """
        .../api/search/
        :return estate list with parameters
    """

    def post(self, request):
        fields = ['province', 'district', 'ward', 'street']
        try:
            page = request.GET.get('page', 1)
            json_data = request.data
            m_keyword = json_data.get('keyword', None)
            m_sort = json_data.get('sort', None)
            m_estate_type = json_data.get('estate_type', None)
            m_filter_max_price = json_data.get('filter_max_price', None)
            m_filter_min_price = json_data.get('filter_min_price', None)
            m_filter_area = json_data.get('filter_area', None)
            m_filter_number_of_room = json_data.get('filter_number_of_room', None)
            m_filter_post_time = json_data.get('filter_post_time', None)

            estate = Estate.objects.all().order_by('-id')
            # --------------- Filter estate type ------------------
            if m_estate_type is not None and m_estate_type != "":
                estate = estate.filter(estateType=m_estate_type)

            # --------------- Search with keyword -----------------
            if m_keyword is not None and m_keyword != "":
                estate = estate.filter(title__icontains=m_keyword)

            # --------------- Filter: Location --------------------
            for field in fields:
                value = json_data.get(field, None)
                if value is not None and value != "":
                    estate = estate.filter(**{field: value})

            # --------------- Filter with max price ---------------
            if m_filter_max_price is not None and m_filter_max_price != "":
                v = FilterMaxPrice.objects.get(id=m_filter_max_price).value
                param = normalize_filter_max_price_param(v)
                if param is not None:
                    estate = estate.filter(price__lte=param)

            # --------------- Filter with min price ---------------
            if m_filter_min_price is not None and m_filter_min_price != "":
                v = FilterMinPrice.objects.get(id=m_filter_min_price).value
                param = normalize_filter_min_price_param(v)
                if param is not None:
                    estate = estate.filter(price__gte=param)

            # --------------- Filter with area ---------------
            if m_filter_area is not None and m_filter_area != "":
                print(m_filter_area)

                v = FilterArea.objects.get(id=m_filter_area).value
                param = normalize_filter_area_param(v)
                if param is not None:
                    estate = estate.filter(area__range=(param[0], param[1]))

            # --------------- Filter with number of room -----
            if m_filter_number_of_room is not None and m_filter_number_of_room != "":
                v = FilterNumberOfRoom.objects.get(id=m_filter_number_of_room).value
                param = normalize_filter_number_of_room_param(v)
                if param is not None:
                    if param != -1:
                        estate = estate.filter(numberOfRoom=param)
                    else:
                        estate = estate.filter(numberOfRoom__range=(6, MAX_INT))

            # --------------- Filter with post time----------------
            if m_filter_post_time is not None and m_filter_post_time != "":
                v = FilterPostTime.objects.get(id=m_filter_post_time).value
                param = normalize_filter_post_time_param(v)
                if param is not None:
                    estate = estate.filter(created_day__range=(param[0], param[1]))

            # --------------- Sort --------------------------------
            if m_sort is not None and m_sort != "":
                v = SortType.objects.get(id=m_sort).value
                param = normalize_sort_param(v)
                if param is not None:
                    estate = estate.order_by(param)

            # --------------- Pagination --------------------------
            paginator = Paginator(estate, ITEMS_PER_PAGE, allow_empty_first_page=True)
            try:
                estate_obj = paginator.page(page)
                serializer = EstateSerializer(estate_obj, context={"request": request}, many=True)
                result = {}
                result['current_page'] = str(page)
                result['total_page'] = str(paginator.num_pages)
                result['result'] = serializer.data
                return Response(result)
            except EmptyPage:
                error_header = {'error_code': EC_FAIL, 'error_message': 'fail - index out of range'}
                return create_json_response(error_header, error_header, status_code=200)

        except KeyError:
            error_header = {'error_code': EC_FAIL, 'error_message': 'Missing require fields'}
            return create_json_response(error_header, error_header, status_code=200)

        except Exception as e:
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


class FavoriteInfo(APIView):
    parser_classes = (MultiPartParser,)

    """
    .../api/favorite/
    get all favorite of current user
    :require user token
    :return
    """
    def get(self, request):
        try:
            # ------------------- Authentication User ---------------------#

            error_header, status_code = Authentication().authentication(request, type_token='user')
            if error_header['error_code'] == 0:
                return create_json_response(error_header, error_header, status_code=status_code)

            user_id = error_header['id']
            page = request.GET.get('page', 1)
            try:
                user_instance = User.objects.get(id=user_id)
                fav_post = Interest.objects.filter(user=user_instance)
                paginator = Paginator(fav_post, ITEMS_PER_PAGE, allow_empty_first_page=True)
                try:
                    fav_post_sub_obj = paginator.page(page)
                    serializer = InterestSerializer(fav_post_sub_obj, context={"request": request}, many=True)
                    result = {}
                    result['current_page'] = str(page)
                    result['total_page'] = str(paginator.num_pages)
                    result['result'] = serializer.data
                    return Response(result)
                except EmptyPage:
                    error_header = {'error_code': EC_FAIL, 'error_message': 'fail - index out of range'}
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

    """
    .../api/favorite/
    get add a favorite estate
    :require user token
    :return
    """
    def post(self, request):
        try:
            # ------------------- Authentication User ---------------------#

            error_header, status_code = Authentication().authentication(request, type_token='user')
            if error_header['error_code'] == 0:
                return create_json_response(error_header, error_header, status_code=status_code)

            user_id = error_header['id']
            json_data = request.data
            estate_id = json_data.get('id')  # required

            try:
                user_instance = User.objects.get(id=user_id)
                estate_instance = Estate.objects.get(id=estate_id)
                exist_fav = Interest.objects.filter(user=user_instance, estate=estate_instance)
                if exist_fav.exists():
                    error_header = {'error_code': EC_FAIL, 'error_message': EM_FAIL + 'Estate is added favorite list'}
                    return create_json_response(error_header, error_header, status_code=200)
                favorite = Interest(user=user_instance, estate=estate_instance)
                favorite.save()

                error_header = {'error_code': EC_SUCCESS, 'error_message': EM_SUCCESS}
                return create_json_response(error_header, error_header, status_code=200)

            except Estate.DoesNotExist:
                error_header = {'error_code': EC_FAIL, 'error_message': 'Estate is not exist'}
                return create_json_response(error_header, error_header, status_code=200)

        except KeyError:
            error_header = {'error_code': EC_FAIL, 'error_message': 'Missing require fields'}
            return create_json_response(error_header, error_header, status_code=200)

        except Exception as e:
            print(e)
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)


    """
    .../api/favorite/
    get remove a favorite estate
    :require user token
    :return
    """
    def delete(self, request):
        try:
            # ------------------- Authentication User ---------------------#

            error_header, status_code = Authentication().authentication(request, type_token='user')
            if error_header['error_code'] == 0:
                return create_json_response(error_header, error_header, status_code=status_code)

            user_id = error_header['id']
            json_data = request.data
            estate_id = json_data.get('id')  # required

            try:
                user_instance = User.objects.get(id=user_id)
                estate_instance = Estate.objects.get(id=estate_id)
                favorite = Interest.objects.get(user=user_instance, estate=estate_instance)
                favorite.delete()

                error_header = {'error_code': EC_SUCCESS, 'error_message': EM_SUCCESS}
                return create_json_response(error_header, error_header, status_code=200)

            except Interest.DoesNotExist:
                error_header = {'error_code': EC_FAIL, 'error_message': 'Interest is not exist'}
                return create_json_response(error_header, error_header, status_code=200)

        except KeyError:
            error_header = {'error_code': EC_FAIL, 'error_message': 'Missing require fields'}
            return create_json_response(error_header, error_header, status_code=200)

        except Exception as e:
            print(e)
            error_header = {'error_code': EC_FAIL, 'error_message': 'fail - ' + str(e)}
            return create_json_response(error_header, error_header, status_code=200)

