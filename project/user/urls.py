from django.conf.urls import url
from django.urls import path
from user.views import *
from . import views

app_name = "user"

urlpatterns = [
    # default homepage
    # url(r'^$', views.index, name='index'),

    # user url
    path('user/', UserInfo.as_view(), name='list_user')
    # path('user/', userinfo)

]
