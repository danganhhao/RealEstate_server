from rest_framework import serializers
from api.models import *
from django.conf import settings

from user.serializers import UserPostSerializer


class EstateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstateType
        fields = '__all__'


class EstateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstateStatus
        fields = '__all__'


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = '__all__'


# ----------------------Get all location-----------------------
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'lat', 'lng')
        # fields = '__all__'


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
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = District
        fields = ['id', 'name', 'wards', 'streets', 'projects']
        # fields = '__all__'


class ProvinceSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True, read_only=True)

    class Meta:
        model = Province
        fields = ['id', 'name', 'code', 'districts']
        # fields = '__all__'


# ----------------------Start get special location-----------------------
class ProvinceSpecialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name', 'code']


class DistrictSpecialSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name', 'prefix']


# ----------------------End get special location-----------------------


class EstateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstateImage
        fields = ['id', 'image']


class EstateSerializer(serializers.ModelSerializer):
    images = EstateImageSerializer(many=True, read_only=True)
    province = serializers.SerializerMethodField('get_province')
    district = serializers.SerializerMethodField('get_district')
    project = serializers.SerializerMethodField('get_project')
    transaction = serializers.SerializerMethodField('get_transaction')

    class Meta:
        model = Estate
        fields = ['id', 'title', 'images', 'province', 'district', 'contact',
                  'project', 'transaction', 'area', 'price', 'created_day', 'lat', 'lng', 'rating']

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

    def get_project(self, estate):
        if estate.project:
            result = {}
            result['id'] = estate.project.id
            result['name'] = estate.project.name
            result['lat'] = estate.project.lat
            result['lng'] = estate.project.lng
            return result
        return ""

    def get_transaction(self, estate):
        if estate.transaction:
            return estate.transaction.name
        return ""


class EstateDetailSerializer(serializers.ModelSerializer):
    images = EstateImageSerializer(many=True, read_only=True)  # related_name = images
    estateType = serializers.SerializerMethodField('get_estateType')
    # estateStatus = serializers.SerializerMethodField('get_estateStatus')
    project = serializers.SerializerMethodField('get_project')
    transaction = serializers.SerializerMethodField('get_transaction')
    province = serializers.SerializerMethodField('get_province')
    district = serializers.SerializerMethodField('get_district')
    ward = serializers.SerializerMethodField('get_ward')
    street = serializers.SerializerMethodField('get_street')

    class Meta:
        model = Estate
        fields = ['id', 'images', 'estateType', 'project', 'transaction', 'province', 'district', 'ward', 'street',
                  'addressDetail', 'title', 'numberOfRoom', 'description', 'detail', 'price', 'area', 'contact',
                  'lat', 'lng', 'rating']
        # fields = '__all__'

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
            result = {}
            result['id'] = estate.project.id
            result['name'] = estate.project.name
            result['lat'] = estate.project.lat
            result['lng'] = estate.project.lng
            return result
        return ""

    def get_transaction(self, estate):
        if estate.transaction:
            return estate.transaction.name
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


class EstateDetailForIsApprovedSerializer(serializers.ModelSerializer):  # only use for get posts of special user
    images = EstateImageSerializer(many=True, read_only=True)  # related_name = images
    estateType = serializers.SerializerMethodField('get_estateType')
    # estateStatus = serializers.SerializerMethodField('get_estateStatus')
    project = serializers.SerializerMethodField('get_project')
    transaction = serializers.SerializerMethodField('get_transaction')
    province = serializers.SerializerMethodField('get_province')
    district = serializers.SerializerMethodField('get_district')
    ward = serializers.SerializerMethodField('get_ward')
    street = serializers.SerializerMethodField('get_street')

    class Meta:
        model = Estate
        fields = ['id', 'images', 'estateType', 'project', 'transaction', 'province', 'district', 'ward', 'street',
                  'addressDetail', 'title', 'numberOfRoom', 'description', 'detail', 'price', 'area', 'contact',
                  'lat', 'lng', 'rating', 'isApproved']
        # fields = '__all__'

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
            result = {}
            result['id'] = estate.project.id
            result['name'] = estate.project.name
            result['lat'] = estate.project.lat
            result['lng'] = estate.project.lng
            return result
        return ""

    def get_transaction(self, estate):
        if estate.transaction:
            return estate.transaction.name
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


class EstateDetailForCurrentUserSerializer(serializers.ModelSerializer):
    images = EstateImageSerializer(many=True, read_only=True)  # related_name = images
    estateType = serializers.SerializerMethodField('get_estateType')
    project = serializers.SerializerMethodField('get_project')
    province = serializers.SerializerMethodField('get_province')
    transaction = serializers.SerializerMethodField('get_transaction')
    district = serializers.SerializerMethodField('get_district')
    ward = serializers.SerializerMethodField('get_ward')
    street = serializers.SerializerMethodField('get_street')

    class Meta:
        model = Estate
        fields = ['id', 'images', 'estateType', 'project', 'transaction', 'province', 'district', 'ward', 'street',
                  'addressDetail', 'title', 'numberOfRoom', 'description', 'detail', 'price', 'area', 'contact',
                  'lat', 'lng', 'rating', 'isApproved']

    def get_estateType(self, estate):
        if estate.estateType:
            result = {}
            result['id'] = estate.estateType.id
            result['name'] = estate.estateType.name
            return result
        return ""

    def get_project(self, estate):
        if estate.project:
            result = {}
            result['id'] = estate.project.id
            result['name'] = estate.project.name
            result['lat'] = estate.project.lat
            result['lng'] = estate.project.lng
            return result
        return ""

    def get_transaction(self, estate):
        if estate.transaction:
            result = {}
            result['id'] = estate.transaction.id
            result['name'] = estate.transaction.name
            return result
        return ""

    def get_province(self, estate):
        if estate.province:
            result = {}
            result['id'] = estate.province.id
            result['name'] = estate.province.name
            return result
        return ""

    def get_district(self, estate):
        if estate.district:
            result = {}
            result['id'] = estate.district.id
            result['name'] = estate.district.name
            return result
        return ""

    def get_ward(self, estate):
        if estate.ward:
            result = {}
            result['id'] = estate.ward.id
            result['name'] = estate.ward.name
            result['prefix'] = estate.ward.prefix
            return result
        return ""

    def get_street(self, estate):
        if estate.street:
            result = {}
            result['id'] = estate.street.id
            result['name'] = estate.street.name
            return result
        return ""


class PostDetailSerializer(serializers.ModelSerializer):
    estate = EstateDetailSerializer()
    user = UserPostSerializer()

    class Meta:
        model = Post
        fields = ['user', 'estate', 'dateFrom', 'dateTo']
        # fields = '__all__'


class PostSerializer(serializers.ModelSerializer):  # For special user, without province_id, district_id...
    estate = EstateDetailForIsApprovedSerializer()

    class Meta:
        model = Post
        fields = ['estate', 'dateFrom', 'dateTo']


class PostForCurrentUserSerializer(serializers.ModelSerializer):  # For current user to edit, need province_id, ...
    estate = EstateDetailForCurrentUserSerializer()

    class Meta:
        model = Post
        fields = ['estate', 'dateFrom', 'dateTo']


class InterestSerializer(serializers.ModelSerializer):
    estate = EstateDetailSerializer()

    class Meta:
        model = Interest
        fields = ['estate']
        # fields = '__all__'


class InterestIDSerializer(serializers.ModelSerializer):
    estate_id = serializers.SerializerMethodField('get_estate_id')

    class Meta:
        model = Interest
        fields = ['estate_id']

    def get_estate_id(self, interest):
        if interest.estate:
            return interest.estate.id
        return ""


class FilterMaxPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterMaxPrice
        fields = ('id', 'name')
        # fields = '__all__'


class FilterMinPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterMinPrice
        fields = ('id', 'name')
        # fields = '__all__'


class FilterAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterArea
        fields = ('id', 'name')
        # fields = '__all__'


class FilterNumberOfRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterNumberOfRoom
        fields = ('id', 'name')
        # fields = '__all__'


class FilterPostTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterPostTime
        fields = ('id', 'name')
        # fields = '__all__'


class SortTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SortType
        fields = ('id', 'name')
        # fields = '__all__'


class NewsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsType
        fields = '__all__'


class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ['id', 'image', 'description']


class NewsSerializer(serializers.ModelSerializer):
    images = NewsImageSerializer(many=True, read_only=True)  # related_name = images
    newsType = serializers.SerializerMethodField('get_newsType')

    class Meta:
        model = News
        fields = ['id', 'title', 'subTitle', 'content', 'newsType', 'images']

    def get_newsType(self, news):
        if news.newsType:
            return news.newsType.name
        return ""


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user')

    class Meta:
        model = Review
        fields = ['id', 'user', 'content', 'rating', 'timestamp']

    def get_user(self, review):
        if review.user:
            result = {}
            result['id'] = review.user.id
            result['name'] = review.user.name
            return result
        return ""


class TodolistSerializer(serializers.ModelSerializer):
    estateType = serializers.SerializerMethodField('get_estateType')
    province = serializers.SerializerMethodField('get_province')
    district = serializers.SerializerMethodField('get_district')

    class Meta:
        model = Todolist
        fields = ['id', 'estateType', 'province', 'district']

    def get_estateType(self, estate):
        if estate.estateType:
            return estate.estateType.name
        return ""

    def get_province(self, estate):
        if estate.province:
            return estate.province.name
        return ""

    def get_district(self, estate):
        if estate.district:
            return estate.district.name
        return ""
