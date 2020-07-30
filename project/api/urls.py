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
    path('s/province/', ProvinceSpecialInfo.as_view(), name='special_province'),
    path('s/district/<int:id>', DistrictSpecialInfo.as_view(), name='special_district'),
    path('s/ward/<int:id>', WardSpecialInfo.as_view(), name='special_ward'),
    path('s/street/<int:id>', StreetSpecialInfo.as_view(), name='special_street'),
    path('s/project/<int:id>', ProjectSpecialInfo.as_view(), name='special_project'),
    path('estatetype/', EstateTypeInfo.as_view(), name='estate_type'),
    path('estatestatus/', EstateStatusInfo.as_view(), name='estate_status'),
    path('project/', ProjectInfo.as_view(), name='project'),
    path('transaction/', TransactionTypeInfo.as_view(), name='transaction'),
    # path('post/$', PostInfo.as_view(), name='post'),
    url(r'^post/$', PostInfo.as_view(), name='post'),
    path('mypost/<int:id>', MyPostInfo.as_view(), name='my_post'),
    url(r'^estate/$', EstateInfo.as_view(), name='estate'),
    # path('estate/$', EstateInfo.as_view(), name='estate'),
    # path('estate/<int:id>', PostDetailInfo.as_view(), name='estate_detail'),
    url(r'estate/(?P<id>[0-9]+)/$', PostDetailInfo.as_view(), name='estate_detail'),
    path('sorttype/', SortTypeInfo.as_view(), name='sort_type'),
    path('filtermaxprice/', FilterMaxPriceInfo.as_view(), name='filter_max_price'),
    path('filterminprice/', FilterMinPriceInfo.as_view(), name='filter_min_price'),
    path('filterarea/', FilterAreaInfo.as_view(), name='filter_area'),
    path('filternumberofroom/', FilterNumberOfRoomInfo.as_view(), name='filter_number_of_room'),
    path('filterposttime/', FilterPostTimeInfo.as_view(), name='filter_post_time'),
    path('search/', SearchEngine.as_view(), name='search'),
    path('searchonmap/', SearchOnMap.as_view(), name='search_on_map'),
    url(r'^postforyou/$', PostForYouInfo.as_view(), name='post_for_you'),
    url(r'^favorite/$', FavoriteInfo.as_view(), name='favorite'),
    path('favoriteid/', FavoriteIDInfo.as_view(), name='favorite_estate_id'),
    url(r'^news/$', NewsInfo.as_view(), name='news'),
    path('cityinfo/', CityInfo.as_view(), name='city_info'),
    path('relatedestate/<int:id>/<int:k>', RelatedEstateInfo.as_view(), name='related_estate'),
    path('rating/', RatingInfo.as_view(), name='rating'),
    path('notification/registertoken/', FCMToken.as_view(), name='register_token'),
    path('notification/markasread/<int:notification_id>', MarkNotiAsRead.as_view(), name='mark_as_read'),
    path('notification/all/', NotificationInfo.as_view(), name='notification'),
    path('review/', ReviewInfo.as_view(), name='review'),
    path('adddata/', AddData.as_view(), name='add_data'),

]
