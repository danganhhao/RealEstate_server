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
    if province_id is None and district_id is None and estate_type is None and price is None and area is None:
        pass
    province_instance = None
    district_instance = None
    estateType_instance = None
    if province_id is not None:
        province_instance = Province.objects.get(id=province_id)
    if district_id is not None:
        district_instance = District.objects.get(id=district_id)
    if estate_type is not None:
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


def getOfferPostsForEachUser(m_id):
    orderby = '-the_count'
    province_instance = None
    district_instance = None
    estateType_instance = None
    list_estate_of_user = Tracking.objects.filter(deviceId=m_id)
    list_province_count = list_estate_of_user.values('province').annotate(the_count=Count('province')).order_by(orderby)
    list_district_count = list_estate_of_user.values('district').annotate(the_count=Count('district')).order_by(orderby)
    list_estateType_count = list_estate_of_user.values('estateType').annotate(the_count=Count('estateType')).order_by(
        orderby)
    list_price_count = list_estate_of_user.values('price').annotate(the_count=Count('price')).order_by(orderby)
    list_area_count = list_estate_of_user.values('area').annotate(the_count=Count('area')).order_by(orderby)

    province_id = list_province_count[0]['province']
    district_id = list_district_count[0]['district']
    estateType_id = list_estateType_count[0]['estateType']
    price_value = list_price_count[0]['price']
    area_value = list_area_count[0]['area']
    area_range = normalize_area_param(area_value)
    price_range = normalize_price_param(price_value)
    if province_id:
        province_instance = Province.objects.get(id=province_id)
    if district_id:
        district_instance = District.objects.get(id=district_id)
    if estateType_id:
        estateType_instance = EstateType.objects.get(id=estateType_id)

    random = randint(0, 2)
    if random == 0:
        print('estateTpye')
        estate = Estate.objects.filter(isApproved=1, province=province_instance, district=district_instance,
                                       estateType=estateType_instance).order_by('-id')[:25]
        serializer = EstateSerializer(estate, many=True)
        return Response(serializer.data)
    if random == 1:
        print('price')
        estate = Estate.objects.filter(isApproved=1, province=province_instance, district=district_instance,
                                       price__range=price_range).order_by('-id')[:25]
        serializer = EstateSerializer(estate, many=True)
        return Response(serializer.data)
    if random == 2:
        print('area')
        estate = Estate.objects.filter(isApproved=1, province=province_instance, district=district_instance,
                                       area__range=area_range).order_by('-id')[:25]
        serializer = EstateSerializer(estate, many=True)
        return Response(serializer.data)
