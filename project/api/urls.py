from django.conf.urls import url
from django.urls import path

from api.views import StreetInfo

urlpatterns = [
    # default homepage
    # url(r'^$', views.index, name='index'),

    # user url
    path('street/', StreetInfo.as_view(), name='street'),

]
