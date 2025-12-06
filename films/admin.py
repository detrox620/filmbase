from django.contrib import admin
from .models import Country, Film, Person, Genre, Rating, Profile
from django.utils import timezone


admin.site.register(Person)
admin.site.register(Country)
admin.site.register(Genre)


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


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('profile', 'film', 'rating', 'created_at', 'updated_at')
    list_filter = ('profile', 'film')


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('name', 'average_rating')
    list_filter = ('name', 'average_rating')