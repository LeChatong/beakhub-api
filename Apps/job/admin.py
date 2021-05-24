from django.contrib import admin

# Register your models here.
from Apps.job.models import Category, Job, PhoneNumber, EmailAddress


class PhoneNumberInlineAdmin(admin.StackedInline):
    model = PhoneNumber
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    extra = 0


class EmailAddressInlineAdmin(admin.StackedInline):
    model = EmailAddress
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display_links = ('slug',)
    list_display = ('slug', 'name', 'status',)
    fieldsets = (
        (None, {'fields': ('name', 'status',)}),
    )


class JobAdmin(admin.ModelAdmin):
    model = Job
    list_display_links = ('slug',)
    list_display = ('slug', 'title', 'token', 'user', 'is_active', 'created_at', 'updated_at',)
    fieldsets = (
        ('Job Information', {'fields': ('title', 'description', 'is_active',)}),
        ('Complementary Information', {'fields': ('user', 'category',)}),
        ('Social Media', {'fields': ('link_facebook', 'link_instagram', 'link_linkedin', 'link_snapchat',
                                     'link_telegram',)}),
    )
    search_fields = ('title',)
    inlines = [PhoneNumberInlineAdmin, EmailAddressInlineAdmin]


class PhoneNumberAdmin(admin.ModelAdmin):
    model = PhoneNumber
    list_display_links = ('phone',)
    list_display = ('phone', 'country', 'has_whatsapp', 'discuss_link', 'is_active', 'created_at', 'updated_at',)


class EmailAddressAdmin(admin.ModelAdmin):
    model = EmailAddress
    list_display_links = ('email',)
    list_display = ('email', 'is_active', 'created_at', 'updated_at',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(PhoneNumber, PhoneNumberAdmin)
admin.site.register(EmailAddress, EmailAddressAdmin)
