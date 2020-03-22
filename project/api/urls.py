from django.conf.urls import url
from django.urls import path

from api.views import *

urlpatterns = [
    # default homepage
    # url(r'^$', views.index, name='index'),

    # user url
    path('location/', LocationInfo.as_view(), name='location'),

]
