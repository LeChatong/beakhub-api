from django.contrib import admin

# Register your models here.
from Apps.comment.models import CommentJob


class CommentJobAdmin(admin.ModelAdmin):

    class Meta:
        model = CommentJob
        fields = '__all__'


admin.site.register(CommentJob, CommentJobAdmin)
