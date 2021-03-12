from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin

from Apps.address.models import Country, City


class CityInlineAdmin(admin.StackedInline):
    model = City
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    extra = 0

class CountryAdmin(ImportExportModelAdmin):
    model = Country
    list_display = ('name', 'phone')
    ordering = ('country',)

    def name(self, obj):
        return obj.name
    name.short_description = 'Name'

    def phone(self, obj):
        return obj.phone_prefix
    phone.short_description = 'Phone Prefix'
    inlines = [CityInlineAdmin,]


class CityAdmin(admin.ModelAdmin):
    model = City
    list_filter = ('country',)
    search_fields = ('name',)


admin.site.register(City, CityAdmin)
admin.site.register(Country, CountryAdmin)
