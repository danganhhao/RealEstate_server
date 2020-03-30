import cv2
import os
from django.core.exceptions import MultipleObjectsReturned

from user.models import User
from django.conf import settings
from rest_framework.authentication import get_authorization_header


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


def get_image_url(request, url):
    if url:
        new_url = url
        if "?" in new_url:
            new_url = settings.MEDIA_URL + url[:url.rfind("?")]
        new_url = request.build_absolute_uri(new_url)
    else:
        new_url = ""
    return new_url
