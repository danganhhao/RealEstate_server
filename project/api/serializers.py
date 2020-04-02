from rest_framework import serializers
from api.models import *
from django.conf import settings


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


class EstateImageSetterSerializer(serializers.ModelSerializer):

    class Meta:
        model = EstateImage
        fields = '__all__'


class EstateImageGetterSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('validate_image_url')

    class Meta:
        model = EstateImage
        fields = ['image']

    def validate_image_url(self, img):
        image = img.image
        if img.image:
            new_url = img.image.url
            if "?" in new_url:
                new_url = settings.MEDIA_URL + image.url[:image.url.rfind("?")]
            request = self.context.get('request')
            new_url = request.build_absolute_uri(new_url)
        else:
            new_url = ""
        return new_url


class EstateSerializer(serializers.ModelSerializer):
    images = EstateImageGetterSerializer(many=True, read_only=True)
    province = serializers.SerializerMethodField('get_province')
    district = serializers.SerializerMethodField('get_district')

    class Meta:
        model = Estate
        fields = ['id', 'title', 'images', 'province', 'district', 'contact']

    # def get_a_image(self, estate):
    #     img = EstateImage.objects.filter(estate=estate.id).first()
    #     serializer = EstateImageGetterSerializer(img)
    #     print(serializer.data)
    #     return serializer.data['image']

    def get_province(self, estate):
        if estate.province:
            return estate.province.name
        return ""

    def get_district(self, estate):
        if estate.district:
            return estate.district.name
        return ""


class EstateDetailSerializer(serializers.ModelSerializer):
    images = EstateImageGetterSerializer(many=True, read_only=True)  # related_name = images
    estateType = serializers.SerializerMethodField('get_estateType')
    estateStatus = serializers.SerializerMethodField('get_estateStatus')
    project = serializers.SerializerMethodField('get_project')
    province = serializers.SerializerMethodField('get_province')
    district = serializers.SerializerMethodField('get_district')
    ward = serializers.SerializerMethodField('get_ward')
    street = serializers.SerializerMethodField('get_street')

    class Meta:
        model = Estate
        fields = '__all__'

    def get_estateType(self, estate):
        if estate.estateType:
            return estate.estateType.name
        return ""

    def get_estateStatus(self, estate):
        if estate.estateStatus:
            return estate.estateStatus.status
        return ""

    def get_project(self, estate):
        if estate.project:
            return estate.project.name
        return ""

    def get_province(self, estate):
        if estate.province:
            return estate.province.name
        return ""

    def get_district(self, estate):
        if estate.district:
            return estate.district.name
        return ""

    def get_ward(self, estate):
        if estate.ward:
            return estate.ward.name
        return ""

    def get_street(self, estate):
        if estate.street:
            return estate.street.name
        return ""


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'


class FilterTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterType
        fields = '__all__'


class SortTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SortType
        fields = '__all__'
