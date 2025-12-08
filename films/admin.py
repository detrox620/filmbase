from django.contrib import admin
from .models import Country, Film, Person, Genre, Rating


admin.site.register(Person)
admin.site.register(Country)
admin.site.register(Genre)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('profile', 'film', 'rating', 'created_at', 'updated_at')
    list_filter = ('profile', 'film')


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('name', 'average_rating')
    list_filter = ('name', 'average_rating')