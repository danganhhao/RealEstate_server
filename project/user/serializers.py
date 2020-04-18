from rest_framework import serializers
from .models import User, UserToken
from django.conf import settings

'''
We'll declare a serializer that we can use to serialize and deserialize an objects.
'''


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'email',
                  'gender', 'birthday', 'address', 'avatar', 'phoneNumber', 'identifyNumber')
        # fields = '__all__'


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToken
        fields = '__all__'
