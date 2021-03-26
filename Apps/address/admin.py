from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin

from Apps.address.models import Country, City, Zone, Address


class CityInlineAdmin(admin.StackedInline):
    model = City
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    extra = 0


class ZoneInlineAdmin(admin.StackedInline):
    model = Zone
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
    inlines = [CityInlineAdmin]


class CityAdmin(admin.ModelAdmin):
    model = City
    list_filter = ('country',)
    list_display_links = ('name',)
    list_display = ('name', 'country', 'is_active',)
    search_fields = ('name',)
    ordering = ('name',)
    inlines = [ZoneInlineAdmin]


class ZoneAdmin(admin.ModelAdmin):
    model = Zone
    list_filter = ('city',)
    list_display_links = ('name',)
    list_display = ('name', 'city', 'is_active',)
    search_fields = ('name',)
    ordering = ('name',)


class AddressAdmin(admin.ModelAdmin):
    model = Address


admin.site.register(Zone, ZoneAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Address, AddressAdmin)
