# -*- coding: utf-8 -*-

from django.db import models


# A model is the single, definitive source of information about your data.
# It contains the essential fields and behaviors of the data you’re storing.
# Generally, each model maps to a single database table.


# Generate media path to upload image
def uploadLocation(instance, filename, **kwargs):
    filePath = 'estate/{title_id}/{filename}'.format(
        title_id=str(instance.title.id), filename=filename
    )
    return filePath


# Create your models here.

# EstateType table (ex:  Unit, Residence, Apartment,..)
class EstateType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# EstateStatus table (ex: bought, sold,...)
class EstateStatus(models.Model):
    status = models.BooleanField()

    def __str__(self):
        return self.status.name


# Project table: describe a project information, include: name, invesloper, constructor,...)
class Project(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


# Type transaction table: buy or sell
class TransactionType(models.Model):
    TYPE = (
        ('B', 'Buy'),
        ('S', 'Sell')
    )
    name = models.CharField(max_length=30, choices=TYPE)

    def __str__(self):
        return self.name


# Province table:
class Province(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=50, null=True)
    code = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name


# District table:
class District(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, null=True)
    prefix = models.CharField(max_length=20, null=True)
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Ward table:
class Ward(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=50, null=True)
    prefix = models.CharField(max_length=20, null=True)
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Street table:
class Street(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, null=True)
    prefix = models.CharField(max_length=20, null=True)
    province_id = models.ForeignKey(Province, on_delete=models.CASCADE)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Estate table: describe an estate information
class Estate(models.Model):
    title = models.CharField(max_length=200)
    estateType = models.ForeignKey(EstateType, on_delete=models.CASCADE)
    estateStatus = models.ForeignKey(EstateStatus, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    transaction = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, null=True, blank=True)
    street = models.ForeignKey(Street, on_delete=models.CASCADE, null=True, blank=True)
    numberOfRoom = models.IntegerField()
    picture = models.ImageField(upload_to=uploadLocation, null=False, blank=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    detail = models.TextField(max_length=5000, null=True, blank=True)
    price = models.BigIntegerField()
    area = models.FloatField()
    contact = models.CharField(max_length=100)

    def __str__(self):
        return self.title


# Post table: when user post a post
class Post(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    dateFrom = models.DateTimeField()
    dateTo = models.DateTimeField()

    def __str__(self):
        return self.estate.name


# Interest table:
class Interest(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name
