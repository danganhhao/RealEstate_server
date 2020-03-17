from django.contrib import admin

# Register your models here.
from user.helper.admin import UserDisplay, UserTokenDisplay
from user.models import *

admin.site.register(User, UserDisplay)
admin.site.register(UserToken, UserTokenDisplay)
admin.site.register(ResetPassword)
