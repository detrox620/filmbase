from django.contrib import admin
from .models import Country, Film, Person, Genre, Rating, Profile
from django.utils import timezone


admin.site.register(Film)
admin.site.register(Person)
admin.site.register(Country)
admin.site.register(Genre)



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'is_ratingban')
    list_filter = ('country', 'is_ratingban')
    actions = ['ban_users', 'unban_users']

    def ban_users(self, request, queryset):
        updated = queryset.update(is_ratingban=timezone.now())
        self.message_user(request, f"{updated} пользователей забанено.")
    ban_users.short_description = "Забанить выбранных"

    def unban_users(self, request, queryset):
        updated = queryset.update(is_ratingban=None)
        self.message_user(request, f"{updated} пользователей разбанено.")
    unban_users.short_description = "Разбанить выбранных"

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('profile', 'film', 'rating', 'created_at', 'updated_at')
    list_filter = ('profile', 'film')
