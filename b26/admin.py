from django.contrib import admin
from .models import UserProfile, FileUpload


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_site_admin']
    list_filter = ['is_site_admin']
    search_fields = ['user__username']

# resources:
# https://docs.djangoproject.com/en/3.2/ref/contrib/admin/


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ['uploader', 'data', 'time_added']
    list_filter = ['time_added', 'uploader']
    search_fields = ['uploader__username', 'data']
