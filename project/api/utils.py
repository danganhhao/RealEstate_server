from django.utils import timezone
from django.conf import settings
from api.models import *
from user.helper.string import TITLE_NOTI
from user.models import *
from pyfcm import FCMNotification


def storage_notification_data(estate_id):
    estate_instance = Estate.objects.get(id=estate_id)
    notification = Notification(
        estateId=estate_instance,
        timestamp=timezone.now()
    )
    notification.save()

    user_id_subscribe_estate = []

    list_user_favorite_of_estate_id = Interest.objects.filter(estate=estate_instance).order_by('-id')
    for fav_obj in list_user_favorite_of_estate_id:
        user_id_subscribe_estate.append(fav_obj.user.id)
        user_instance = User.objects.get(id=fav_obj.user.id)

        notification_data = NotificationData(
            userId=user_instance,
            notificationId=notification,
            state=False
        )
        notification_data.save()

    return notification, user_id_subscribe_estate


def get_body(notification):
    data_body = {
        'id': str(notification.id),
        'title': TITLE_NOTI,
        'body': "Bất động sản \"" + str(notification.estateId.title) + "\" gần đây đã được cập nhật thông tin mới.",
        'estate_id': str(notification.estateId.id),
        'timestamp': str(notification.timestamp),
        'state': "False"
    }
    return data_body


def send_notification(estate_id):
    notification, user_id_subscribe_estate = storage_notification_data(estate_id)
    user_noti_token = UserNotiToken.objects.filter(userId__in=user_id_subscribe_estate)
    list_user_noti_token = []
    for item in user_noti_token:
        list_user_noti_token.append(item.token)

    data_body = get_body(notification)
    push_service = FCMNotification(api_key=settings.FIREBASE_SERVER_KEY)

    message_title = TITLE_NOTI
    message_body = "Bất động sản \"" + str(notification.estateId.title) + "\" gần đây đã được cập nhật thông tin mới."

    result = push_service.notify_multiple_devices(registration_ids=list_user_noti_token, message_title=message_title,
                                                  message_body=message_body, data_message=data_body)

    print(result)
