from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_vip', 'vip_expire_date', 'member_since']
    list_filter = ['is_vip', 'member_since']
    search_fields = ['user__username', 'user__email']
