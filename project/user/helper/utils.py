import cv2
import os
from django.core.exceptions import MultipleObjectsReturned

from user.models import User, UserToken


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
