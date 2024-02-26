from django.contrib import admin

from .models import UserProfile

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_site_admin']
    list_filter = ['is_site_admin']
    search_fields = ['user__username']
