from django.conf.urls import url
from django.urls import path
from user.views import *
from . import views

app_name = "user"

urlpatterns = [
    # default homepage
    # url(r'^$', views.index, name='index'),

    # user url
    path('user/', UserInfo.as_view(), name='user'),
    path('user/login/', Login.as_view(), name='login'),
    path('user/logout/', Logout.as_view(), name='logout'),
    path('user/forgot/', ForgotPassword.as_view(), name='forgot_password'),
    path('user/reset/', ResetPassword.as_view(), name='reset_password'),
    path('user/password/', ChangePassword.as_view(), name='change_password'),
    path('user/checkingaccount/', RegisterAgency.as_view(), name='checking_account'),
    path('user/agency/', AgencyInfo.as_view(), name='agency')

]
