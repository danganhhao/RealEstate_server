from django.contrib import admin

"""
    Custom view of admin page
"""


class UserDisplay(admin.ModelAdmin):
    list_display = ('username', 'email', 'name', 'gender')
    list_display_links = ('username', 'email')
    search_fields = ('username', 'email')
    list_per_page = 25


class UserTokenDisplay(admin.ModelAdmin):
    list_display = ('user', 'token',)
    list_display_links = ('user',)
    search_fields = ('user',)
    list_per_page = 25
