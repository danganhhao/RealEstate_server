import jwt
from django.conf import settings
from django.utils import timezone


def create_admin_token(id, email):
    payload = {
        'type': 'admin',
        'id': id,
        'email': email,
        'create_time': timezone.now().isoformat()
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode()
    return token
