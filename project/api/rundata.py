"""
python manage.py shell < api/rundata.py

"""
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

import csv

# ------------------- Get Parameters ---------------------#
user_id = 28

print("AAA")
reader = csv.DictReader(open("/home/danganhhaotest/RealEstate_server/realestate_data_100.csv"))
for raw in reader:
    title = raw.get('title')  # required
    estateType = raw.get('estateType')  # required
    expire_after = raw.get('expireAfter')  # required
    project = raw.get('project', None)
    province = raw.get('province')  # required
    district = raw.get('district')  # required
    ward = raw.get('ward', None)
    street = raw.get('street', None)
    address_detail = raw.get('addressDetail', "")
    numberOfRoom = raw.get('numberOfRoom', "")
    description = raw.get('description')  # required
    detail = raw.get('detail')
    price = raw.get('price', "")
    area = raw.get('area', "")
    contact = raw.get('contact', "")
    images = raw.get('image', "")
    transaction = raw.get('transaction')  # required
    lat = raw.get('lat', 0)
    lng = raw.get('lng', 0)

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
        transaction_instance = TransactionType.objects.get(id=transaction)
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
        if expireDays > 365:
            expireDays = 365
        if lat == "":
            lat = 0
        if lng == "":
            lng = 0

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
            transaction=transaction_instance,
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
        if images:
            path = uploadLocationEstate(estate_id, len(images))
            upload_data = cloudinary.uploader.upload(images, public_id=path)
            estate_image = EstateImage(
                estate=estate,
                image=upload_data['secure_url']
            )
            estate_image.save()

        # ------------------- Create Post ---------------------#
        user_instance = User.objects.get(id=user_id)

        new_post = Post(
            user=user_instance,
            estate=estate,
            dateFrom=timezone.now(),
            dateTo=(timezone.now() + timezone.timedelta(days=expireDays))
        )
        new_post.save()

        print('Done - ' + str(estate.id))

    except EstateType.DoesNotExist:
        error_header = {'error_code': EC_FAIL, 'error_message': ' fail'}


if __name__ == "__main__":
    print("AA")
