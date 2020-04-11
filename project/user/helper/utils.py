import cv2
import os

from django.core.exceptions import MultipleObjectsReturned
from django.utils import timezone
from django.conf import settings

from rest_framework.authentication import get_authorization_header

from user.models import User
from user.helper.string import *


def is_username_exist(username):
    try:
        User.objects.get(username=username)
        return True
    except MultipleObjectsReturned:
        return True
    except User.DoesNotExist:
        return False


def is_email_exist(email):
    try:
        User.objects.get(email=email)
        return True

    except MultipleObjectsReturned:
        return True
    except User.DoesNotExist:
        return False


def is_image_aspect_ratio_valid(img_url):
    img = cv2.imread(img_url)
    dimensions = tuple(img.shape[1::-1])  # return: (width, height)
    aspect_ratio = dimensions[0] / dimensions[1]  # divide w/h
    if aspect_ratio < 1:
        return False
    return True


def is_image_size_valid(img_url, mb_limit):
    img_size = os.path.getsize(img_url)
    if img_size > mb_limit:
        return False
    return True


def get_token(request):
    # return request.META.get('HTTP_AUTHORIZATION', b'').replace("Bearer ", "")
    auth = get_authorization_header(request).split()
    return auth[1].decode("utf-8")


def get_image_url(request, avatar):
    if avatar != "":
        new_url = avatar.url
        if "?" in new_url:
            new_url = settings.MEDIA_URL + avatar.url[:avatar.url.rfind("?")]
        new_url = request.build_absolute_uri(new_url)
    else:
        new_url = ""
    return new_url


def normalize_filter_max_price_param(filter_id):
    switcher = {
        1: None,
        2: 500,  # million
        3: 800,
        4: 1000,
        5: 2000,
        6: 3000,
        7: 5000,
        8: 7000,
        9: 10000,
        10: 15000,
        11: 30000,
    }
    return switcher.get(filter_id, None)


def normalize_filter_min_price_param(filter_id):
    switcher = {
        1: None,
        2: 500,  # million
        3: 800,
        4: 1000,
        5: 2000,
        6: 3000,
        7: 5000,
        8: 7000,
        9: 10000,
        10: 15000,
        11: 30000,
    }
    return switcher.get(filter_id, None)


def normalize_filter_area_param(filter_id):
    switcher = {
        1: None,
        2: (0, 30),
        3: (30, 50),
        4: (50, 70),
        5: (70, 100),
        6: (100, 150),
        7: (150, 250),
        8: (250, 500),
        9: (500, 1000),
        10: (1000, 2000),
        11: (2000, MAX_INT),
    }
    return switcher.get(filter_id, None)


def normalize_filter_number_of_room_param(filter_id):
    switcher = {
        1: None,
        2: 1,
        3: 2,
        4: 3,
        5: 4,
        6: 5,
        7: -1,
    }
    return switcher.get(filter_id, None)


def normalize_filter_post_time_param(filter_id):
    switcher = {
        1: None,
        2: (str(timezone.now() - timezone.timedelta(days=1)), str(timezone.now())),
        3: (str(timezone.now() - timezone.timedelta(days=3)), str(timezone.now())),
        4: (str(timezone.now() - timezone.timedelta(days=7)), str(timezone.now())),
        5: (str(timezone.now() - timezone.timedelta(days=15)), str(timezone.now())),
        6: (str(timezone.now() - timezone.timedelta(days=30)), str(timezone.now())),
    }
    return switcher.get(filter_id, None)


def normalize_sort_param(sort_id):
    switcher = {
        "1": None,
        "2": "-created_day",
        "3": "price",
        "4": "-price",
        "5": "area",
        "6": "-area"
    }
    return switcher.get(sort_id, None)
