from rest_framework import serializers
from .models import User

'''
We'll declare a serializer that we can use to serialize and deserialize an objects.
'''


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ('username', 'email')
        fields = '__all__'

    # name = serializers.CharField(max_length=100)
    # username = serializers.CharField(max_length=50, unique=True)
    # password = serializers.CharField(max_length=300)
    # address = serializers.CharField(max_length=300)
    # phoneNumber = serializers.CharField(max_length=15)
    # emailAddress = serializers.EmailField(null=True, blank=True)
    # identifyNumber = serializers.CharField(max_length=15, null=True, blank=True)
    #
    # def create(self, validated_data):
    #     return User.objects.create(validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.username = validated_data.get('username', instance.username)
    #     instance.password = validated_data.get('password', instance.password)
    #     instance.address = validated_data.get('address', instance.address)
    #     instance.phoneNumber = validated_data.get('phoneNumber', instance.phoneNumber)
    #     instance.emailAddress = validated_data.get('emailAddress', instance.emailAddress)
    #     instance.identifyNumber = validated_data.get('identifyNumber', instance.identifyNumber)
    #     instance.save()
    #     return instance
