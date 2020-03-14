from django.contrib import admin

# Register your models here.
from api.models import *

admin.site.register(TransactionType)
admin.site.register(Post)
admin.site.register(Interest)
admin.site.register(EstateStatus)
admin.site.register(Estate)
admin.site.register(EstateType)
admin.site.register(Location)
admin.site.register(Project)
