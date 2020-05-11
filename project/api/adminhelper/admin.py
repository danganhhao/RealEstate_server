from django.contrib import admin

"""
    Custom view of admin page
"""


# ------------------------------------------

class EstateFilter(admin.SimpleListFilter):
    """
    Reference: https://medium.com/elements/getting-the-most-out-of-django-admin-filters-2aecbb539c9a
    """
    title = 'IsApproved'
    parameter_name = 'isApproved'

    def lookups(self, request, model_admin):
        list_of_estates = [('True', "Approved"), ('False', "Not Approved")]
        return sorted(list_of_estates, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        value = super(EstateFilter, self).value()
        if value is not None:
            return queryset.filter(isApproved=value)
        return queryset


# --------------------------------------

class ProvinceDisplay(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'code')
    list_per_page = 25


class DistrictDisplay(admin.ModelAdmin):
    list_display = ('id', 'name', 'prefix', 'province_id')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'code')
    list_per_page = 25


class WardDisplay(admin.ModelAdmin):
    list_display = ('id', 'name', 'prefix', 'province_id', 'district_id')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'code')
    list_per_page = 25


class StreetDisplay(admin.ModelAdmin):
    list_display = ('id', 'name', 'prefix', 'province_id', 'district_id')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'code')
    list_per_page = 25


class ProjectDisplay(admin.ModelAdmin):
    list_display = ('id', 'name', 'lat', 'lng', 'province_id', 'district_id')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'code')
    list_per_page = 25


class EstateDisplay(admin.ModelAdmin):
    list_display = ('id', 'title', 'estateType', 'project', 'province', 'district', 'isApproved')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', 'province__name', 'district__name', 'isApproved')
    list_per_page = 25
    list_filter = (EstateFilter,)

    actions = ['do_approve_estate', ]
    # TODO: Override delete_estates, delete in post table, and delete image in cloud

    def do_approve_estate(self, request, queryset):
        count = queryset.update(isApproved=True)
        self.message_user(request, '{} estate(s) have been approved successfully.'.format(count))

    do_approve_estate.short_description = 'Mark selected estates as published'


class EstateImageDisplay(admin.ModelAdmin):
    list_display = ('id', 'estate', 'image')
    list_display_links = ('id', 'estate')
    search_fields = ('id', 'estate__id')
    list_per_page = 25


class PostDisplay(admin.ModelAdmin):
    list_display = ('id', 'user', 'estate', 'transaction', 'dateFrom', 'dateTo')
    list_display_links = ('id', 'user', 'estate')
    search_fields = ('id', 'user__name', 'estate__title', 'transaction__name')
    list_per_page = 25


class InterestDisplay(admin.ModelAdmin):
    list_display = ('id', 'user', 'estate')
    list_display_links = ('id', 'user', 'estate')
    search_fields = ('id', 'user__name', 'estate__id')
    list_per_page = 25


class NewsDisplay(admin.ModelAdmin):
    list_display = ('id', 'title', 'newsType')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', 'newsType__name')
    list_per_page = 25


class NewsImageDisplay(admin.ModelAdmin):
    list_display = ('id', 'news', 'image')
    list_display_links = ('id', 'news')
    search_fields = ('id', 'news__title')
    list_per_page = 25