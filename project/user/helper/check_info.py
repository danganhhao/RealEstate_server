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
