from rest_framework import serializers
from api.models import *


class EstateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstateType
        fields = '__all__'


class EstateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstateStatus
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = '__all__'


class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = ('id', 'name', 'prefix')
        # fields = '__all__'


class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = ('id', 'name', 'prefix')
        # fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    wards = WardSerializer(many=True, read_only=True)
    streets = StreetSerializer(many=True, read_only=True)

    class Meta:
        model = District
        fields = ['id', 'name', 'wards', 'streets']
        # fields = '__all__'


class ProvinceSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True, read_only=True)

    class Meta:
        model = Province
        fields = ['id', 'name', 'code', 'districts']
        # fields = '__all__'


class EstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estate
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'
