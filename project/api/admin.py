from django.contrib import admin

# Register your models here.
from api.models import *
from api.adminhelper.admin import *

admin.site.register(TransactionType)
admin.site.register(Post, PostDisplay)
admin.site.register(Interest, InterestDisplay)
admin.site.register(EstateStatus)
admin.site.register(Estate, EstateDisplay)
admin.site.register(EstateImage, EstateImageDisplay)
admin.site.register(EstateType)
admin.site.register(Project, ProjectDisplay)
admin.site.register(Province, ProvinceDisplay)
admin.site.register(District, DistrictDisplay)
admin.site.register(Ward, WardDisplay)
admin.site.register(Street, StreetDisplay)
admin.site.register(FilterMaxPrice)
admin.site.register(FilterMinPrice)
admin.site.register(FilterArea)
admin.site.register(FilterNumberOfRoom)
admin.site.register(FilterPostTime)
admin.site.register(SortType)
admin.site.register(NewsType)
admin.site.register(NewsImage, NewsImageDisplay)
admin.site.register(News, NewsDisplay)
admin.site.register(Tracking, TrackingDisplay)
admin.site.register(Notification)
admin.site.register(UserNotiToken)
admin.site.register(NotificationData)
admin.site.register(Review)
admin.site.register(RatingType)
admin.site.register(Rating)
