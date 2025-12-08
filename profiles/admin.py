from django.contrib import admin
from .models import Profile
from django.utils import timezone



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'is_ratingban')
    list_filter = ('country', 'is_ratingban')
    actions = ['ban_users', 'unban_users']

    def ban_users(self, request, queryset):
        for profile in queryset:
            profile.is_ratingban = timezone.now()
            profile.save()
        self.message_user(request, f"{queryset.count()} пользователей забанено.")
    ban_users.short_description = "Забанить выбранных"

    def unban_users(self, request, queryset):
        for profile in queryset:
            profile.is_ratingban = None
            profile.save()
        self.message_user(request, f"{queryset.count()} пользователей разбанено.")
    unban_users.short_description = "Разбанить выбранных"