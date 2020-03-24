from django.conf.urls import url
from django.urls import path

from api.views import *

urlpatterns = [
    # default homepage
    # url(r'^$', views.index, name='index'),

    # user url
    path('location/', ProvinceInfo.as_view(), name='location'),
    path('province/', ProvinceInfo.as_view(), name='province'),
    path('province/<int:id>', ProvinceDetailInfo.as_view(), name='province_detail'),
    path('province/<int:p_id>/district/<int:d_id>', DistrictDetailInfo.as_view(), name='district_detail'),

]
