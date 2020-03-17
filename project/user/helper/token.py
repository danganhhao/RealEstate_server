import jwt
from django.conf import settings
from django.utils import timezone


def create_token(model_instance, model_type):
    """
    :param model_instance: Object need to be created token
    :param model_type: user/admin
    :return token in string
    """

    payload = {
        'type': model_type,
        'id': model_instance.username,
        'email': model_instance.email,
        'create_time': timezone.now().isoformat()
    }

    # generate token
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode()

    model_instance.usertoken_set.create(
        token=token,
    )

    model_instance.save()
    return {'token': token}
