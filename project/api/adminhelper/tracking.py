"""
    Tracking helper: Record user behavior and save into tracking table
    in order to offer accordant real estate posts for each user
"""
from random import randint

from api.models import *
from api.serializers import *
from django.utils import timezone
from rest_framework.response import Response
from django.db.models import Count

from user.helper.string import MAX_INT
from user.helper.utils import isExistObject


class Switch(dict):
    def __getitem__(self, item):
        for key in self.keys():
            if item in key:
                return super().__getitem__(key)
        return (0, MAX_INT)


def saveToDatabase(m_id, province_id, district_id, estate_type, price, area):
    """
        :param m_id (user_id or device_id)
        :param province_id (to save into tracking table)
        :param district_id (to save into tracking table)
        :param estate_type (to save into tracking table)
        :param price (to save into tracking table)
        :param area (to save into tracking table)
        :return
    """
    if isExistObject(province_id) == False \
            and isExistObject(district_id) == False \
            and isExistObject(estate_type) == False \
            and isExistObject(price) == False \
            and isExistObject(area) == False:
        return
    province_instance = None
    district_instance = None
    estateType_instance = None
    if isExistObject(province_id):
        province_instance = Province.objects.get(id=province_id)
    if isExistObject(district_id):
        district_instance = District.objects.get(id=district_id)
    if isExistObject(estate_type):
        estateType_instance = EstateType.objects.get(id=estate_type)
    Tracking(
        deviceId=m_id,
        province=province_instance,
        district=district_instance,
        estateType=estateType_instance,
        price=price,
        area=area,
        timestamp=timezone.now()).save()


def normalize_area_param(value):
    switch = Switch({
        range(0, 30): (0, 30),
        range(30, 50): (30, 50),
        range(50, 70): (50, 70),
        range(70, 100): (70, 100),
        range(100, 150): (100, 150),
        range(150, 250): (150, 250),
        range(250, 500): (250, 500),
        range(500, 1000): (500, 1000),
        range(1000, 2000): (1000, 2000),
        range(2000, MAX_INT): (2000, MAX_INT),
    })
    return switch[value]


def normalize_price_param(value):
    min_value = value - 1000
    if min_value < 0:
        min_value = 0
    max_value = value + 1000
    return (min_value, max_value)


def returnDefaultList():
    estate = Estate.objects.filter(isApproved=1).order_by('-id')[:25]
    serializer = EstateSerializer(estate, many=True)
    return serializer.data


def returnWithParam(province_id, district_id, estateType_id):
    province_instance = None
    district_instance = None
    estateType_instance = None

    if province_id:
        province_instance = Province.objects.get(id=province_id)
    if district_id:
        district_instance = District.objects.get(id=district_id)
    if estateType_id:
        estateType_instance = EstateType.objects.get(id=estateType_id)

    if province_instance is not None and district_instance is None and estateType_instance is None:
        estate = Estate.objects.filter(isApproved=1, province=province_instance).order_by('-id')[:25]
        serializer = EstateSerializer(estate, many=True)
        return serializer.data
    if province_instance is None and district_instance is not None and estateType_instance is None:
        estate = Estate.objects.filter(isApproved=1, district=district_instance).order_by('-id')[:25]
        serializer = EstateSerializer(estate, many=True)
        return serializer.data
    if province_instance is None and district_instance is None and estateType_instance is not None:
        estate = Estate.objects.filter(isApproved=1, estateType=estateType_instance).order_by('-id')[:25]
        serializer = EstateSerializer(estate, many=True)
        return serializer.data
    if province_instance is not None and district_instance is not None and estateType_instance is None:
        estate = Estate.objects.filter(isApproved=1, province=province_instance,
                                       district=district_instance).order_by('-id')[:25]
        serializer = EstateSerializer(estate, many=True)
        return serializer.data
    if province_instance is not None and district_instance is None and estateType_instance is not None:
        estate = Estate.objects.filter(isApproved=1, province=province_instance,
                                       estateType=estateType_instance).order_by('-id')[:25]
        serializer = EstateSerializer(estate, many=True)
        return serializer.data
    if province_instance is None and district_instance is not None and estateType_instance is not None:
        estate = Estate.objects.filter(isApproved=1, district=district_instance,
                                       estateType=estateType_instance).order_by('-id')[:25]
        serializer = EstateSerializer(estate, many=True)
        return serializer.data
    if province_instance is not None and district_instance is not None and estateType_instance is not None:
        estate = Estate.objects.filter(isApproved=1, province=province_instance, district=district_instance,
                                       estateType=estateType_instance).order_by('-id')[:25]
        serializer = EstateSerializer(estate, many=True)
        return serializer.data


def getOfferPostsForEachUser(m_id):
    result = []
    orderby = '-the_count'
    province_instance = None
    district_instance = None
    estateType_instance = None
    list_estate_of_user = Tracking.objects.filter(deviceId=m_id)
    if list_estate_of_user:
        list_province_count = list_estate_of_user.values('province').annotate(the_count=Count('province')).order_by(
            orderby)
        list_district_count = list_estate_of_user.values('district').annotate(the_count=Count('district')).order_by(
            orderby)
        list_estateType_count = list_estate_of_user.values('estateType').annotate(
            the_count=Count('estateType')).order_by(
            orderby)
        list_price_count = list_estate_of_user.values('price').annotate(the_count=Count('price')).order_by(orderby)
        list_area_count = list_estate_of_user.values('area').annotate(the_count=Count('area')).order_by(orderby)

        if list_province_count is None:
            return returnDefaultList()
        if list_district_count is None:
            return returnDefaultList()
        if list_estateType_count is None:
            return returnDefaultList()
        if list_price_count is None:
            return returnDefaultList()
        if list_area_count is None:
            return returnDefaultList()
        province_id = list_province_count[0]['province']
        district_id = list_district_count[0]['district']
        estateType_id = list_estateType_count[0]['estateType']
        price_value = list_price_count[0]['price']
        area_value = list_area_count[0]['area']
        if area_value:
            area_range = normalize_area_param(area_value)
        else:
            area_range = None
        if price_value:
            price_range = normalize_price_param(price_value)
        else:
            price_range = None

        if province_id is not None and district_id is not None and estateType_id is not None \
                and price_range is not None and area_range is not None:
            if province_id:
                province_instance = Province.objects.get(id=province_id)
            if district_id:
                district_instance = District.objects.get(id=district_id)
            if estateType_id:
                estateType_instance = EstateType.objects.get(id=estateType_id)

            random = randint(0, 2)
            if random == 0:
                estate = Estate.objects.filter(isApproved=1, province=province_instance, district=district_instance,
                                               estateType=estateType_instance).order_by('-id')[:25]
                serializer = EstateSerializer(estate, many=True)
                result = serializer.data
            if random == 1:
                estate = Estate.objects.filter(isApproved=1, province=province_instance, district=district_instance,
                                               price__range=price_range).order_by('-id')[:25]
                serializer = EstateSerializer(estate, many=True)
                result = serializer.data
            if random == 2:
                estate = Estate.objects.filter(isApproved=1, province=province_instance, district=district_instance,
                                               area__range=area_range).order_by('-id')[:25]
                serializer = EstateSerializer(estate, many=True)
                result = serializer.data
            if len(result) == 0:
                return returnWithParam(province_id, district_instance, estateType_id)
            else:
                return result
        else:
            return returnWithParam(province_id, district_instance, estateType_id)
    else:
        return returnDefaultList()
