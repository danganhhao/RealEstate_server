from django.forms import DateField
from rest_framework import serializers
from .models import User, UserToken
from django.conf import settings

'''
We'll declare a serializer that we can use to serialize and deserialize an objects.
'''


class UserSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(format="%d/%m/%Y")

    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'email',
                  'gender', 'birthday', 'address', 'avatar', 'phoneNumber', 'identifyNumber', 'isAgency')
        # fields = '__all__'


# For post
class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'phoneNumber', 'isAgency')


class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToken
        fields = '__all__'
