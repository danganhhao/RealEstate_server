from rest_framework import serializers
from .models import User, UserToken
from django.conf import settings

'''
We'll declare a serializer that we can use to serialize and deserialize an objects.
'''


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('validate_image_url')

    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'email',
                  'gender', 'birthday', 'address', 'avatar', 'phoneNumber', 'identifyNumber')
        # fields = '__all__'

    def validate_image_url(self, user):
        avatar = user.avatar
        if user.avatar:
            new_url = user.avatar.url
            if "?" in new_url:
                new_url = settings.MEDIA_URL + avatar.url[:avatar.url.rfind("?")]
            request = self.context.get('request')
            new_url = request.build_absolute_uri(new_url)
        else:
            new_url = ""
        return new_url


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToken
        fields = '__all__'
