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
    path('estatetype/', EstateTypeInfo.as_view(), name='estate_type'),
    path('estatestatus/', EstateStatusInfo.as_view(), name='estate_status'),
    path('project/', ProjectInfo.as_view(), name='project'),
    path('transaction/', TransactionTypeInfo.as_view(), name='transaction'),
    path('post/', PostInfo.as_view(), name='post'),
    path('estate/', EstateInfo.as_view(), name='estate'),
    path('estate/<int:id>', EstateDetailInfo.as_view(), name='estate_detail')

]
