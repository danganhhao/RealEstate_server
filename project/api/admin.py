from django.contrib import admin

# Register your models here.
from api.models import *

admin.site.register(TransactionType)
admin.site.register(Post)
admin.site.register(Interest)
admin.site.register(EstateStatus)
admin.site.register(Estate)
admin.site.register(EstateType)
admin.site.register(Project)
admin.site.register(Province)
admin.site.register(District)
admin.site.register(Ward)
admin.site.register(Street)
