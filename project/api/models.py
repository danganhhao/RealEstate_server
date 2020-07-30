# -*- coding: utf-8 -*-

from django.db import models


# A model is the single, definitive source of information about your data.
# It contains the essential fields and behaviors of the data you’re storing.
# Generally, each model maps to a single database table.


# Generate media path to upload image
def uploadLocation(instance, filename, **kwargs):
    filePath = 'estate/{estate_id}/{filename}'.format(
        estate_id=str(instance.estate), filename=filename
    )
    return filePath


# Create your models here.

# EstateType table (ex:  Unit, Residence, Apartment,..)
class EstateType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_id(self):
        return self.id


# EstateStatus table (ex: bought, sold,...)
class EstateStatus(models.Model):
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.status

    def get_id(self):
        return self.id


# Type transaction table: buy or sell
class TransactionType(models.Model):
    TYPE = (
        ('Thuê', 'Thuê'),
        ('Bán', 'Bán')
    )
    name = models.CharField(max_length=30, choices=TYPE)

    def __str__(self):
        return self.name

    def get_id(self):
        return self.id


# Province table:
class Province(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=50, null=True)
    code = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name

    def get_id(self):
        return self.id


# District table:
class District(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, null=True)
    prefix = models.CharField(max_length=20, null=True)
    province_id = models.ForeignKey(Province, related_name='districts', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_id(self):
        return self.id


# Ward table:
class Ward(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=50, null=True)
    prefix = models.CharField(max_length=20, null=True)
    province_id = models.ForeignKey(Province, related_name='wards', on_delete=models.CASCADE)
    district_id = models.ForeignKey(District, related_name='wards', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Street table:
class Street(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, null=True)
    prefix = models.CharField(max_length=20, null=True)
    province_id = models.ForeignKey(Province, related_name='streets', on_delete=models.CASCADE)
    district_id = models.ForeignKey(District, related_name='streets', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Project table: describe a project information, include: name, invesloper, constructor,...)
class Project(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=50, null=True)
    province_id = models.ForeignKey(Province, related_name='projects', on_delete=models.CASCADE)
    district_id = models.ForeignKey(District, related_name='projects', on_delete=models.CASCADE)
    lat = models.FloatField(default=0, null=True)
    lng = models.FloatField(default=0, null=True)

    def __str__(self):
        return self.name


# Estate table: describe an estate information
class Estate(models.Model):
    title = models.CharField(max_length=200)
    estateType = models.ForeignKey(EstateType, on_delete=models.CASCADE)
    estateStatus = models.ForeignKey(EstateStatus, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, null=True, blank=True)
    street = models.ForeignKey(Street, on_delete=models.CASCADE, null=True, blank=True)
    transaction = models.ForeignKey(TransactionType, on_delete=models.CASCADE, null=True)
    addressDetail = models.CharField(max_length=100, null=True, blank=True)
    numberOfRoom = models.IntegerField()
    description = models.TextField(max_length=5000, null=True, blank=True)
    detail = models.TextField(max_length=5000, null=True, blank=True)
    price = models.BigIntegerField()
    area = models.FloatField()
    contact = models.CharField(max_length=100)
    created_day = models.DateTimeField()
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)
    rating = models.FloatField(default=0)
    isApproved = models.IntegerField(default=2)

    def __str__(self):
        return str(self.id)


# EstateImage: contain all images of a special estate
class EstateImage(models.Model):
    estate = models.ForeignKey(Estate, related_name='images', on_delete=models.CASCADE)
    # image = models.ImageField(upload_to=uploadLocation, null=False, blank=True)
    image = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.id)


# Post table: when user post a post
class Post(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    dateFrom = models.DateTimeField()
    dateTo = models.DateTimeField()

    def __str__(self):
        return str(self.estate.id)


# Interest table:
class Interest(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name


# Filter max price table:
class FilterMaxPrice(models.Model):
    name = models.CharField(max_length=30)
    value = models.IntegerField()

    def __str__(self):
        return self.name


# Filter min price table:
class FilterMinPrice(models.Model):
    name = models.CharField(max_length=30)
    value = models.IntegerField()

    def __str__(self):
        return self.name


# Filter area table:
class FilterArea(models.Model):
    name = models.CharField(max_length=30)
    value = models.IntegerField()

    def __str__(self):
        return self.name


# Filter number of room table:
class FilterNumberOfRoom(models.Model):
    name = models.CharField(max_length=30)
    value = models.IntegerField()

    def __str__(self):
        return self.name


# Filter post time table:
class FilterPostTime(models.Model):
    name = models.CharField(max_length=30)
    value = models.IntegerField()

    def __str__(self):
        return self.name


# Sort type table:
class SortType(models.Model):
    name = models.CharField(max_length=30)
    value = models.IntegerField()

    def __str__(self):
        return self.name


# News Type table (ex:  Normal,...)
class NewsType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# News table: describe an news information
class News(models.Model):
    title = models.CharField(max_length=200)
    subTitle = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    newsType = models.ForeignKey(NewsType, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)


# NewsImage: contain all images of a news
class NewsImage(models.Model):
    news = models.ForeignKey(News, related_name='images', on_delete=models.CASCADE)
    image = models.CharField(max_length=300, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.id)


# Tracking table:
class Tracking(models.Model):
    deviceId = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
    estateType = models.ForeignKey(EstateType, on_delete=models.CASCADE, null=True, blank=True)
    price = models.BigIntegerField(null=True, blank=True)
    area = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField()

    def __str__(self):
        return str(self.deviceId)


# Notification System

# Notification table:
class Notification(models.Model):
    estateId = models.ForeignKey(Estate, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField()

    def __str__(self):
        return str(self.id)


# UserNotiToken table
class UserNotiToken(models.Model):
    userId = models.ForeignKey('user.User', on_delete=models.CASCADE)
    token = models.CharField(max_length=500)

    def __str__(self):
        return str(self.id)


# NotificationData table
class NotificationData(models.Model):
    userId = models.ForeignKey('user.User', on_delete=models.CASCADE)
    notificationId = models.ForeignKey(Notification, on_delete=models.CASCADE)
    state = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


# Review table
class Review(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    content = models.TextField(max_length=5000)
    rating = models.IntegerField(default=0)
    timestamp = models.DateTimeField()

    def __str__(self):
        return str(self.id)


# Rating type table
class RatingType(models.Model):
    name = models.TextField(max_length=30)
    value = models.IntegerField()

    def __str__(self):
        return str(self.name)


# Rating table
class Rating(models.Model):
    deviceId = models.CharField(max_length=100)  # user_id
    estateId = models.CharField(max_length=100)
    ratingType = models.ForeignKey(RatingType, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)
