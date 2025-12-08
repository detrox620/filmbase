from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Rating
from profiles.models import Profile


@receiver(post_save, sender=Rating)
def update_rating(sender, instance, created, **kwargs):
    film = instance.film
    ratings = film.rating_set.all()
    sum = 0
    count = 0
    for rating in ratings:
        if not rating.profile.is_ratingban:
            sum += rating.rating
            count += 1
    if count == 0:
        film.average_rating = None
    else:
        film.average_rating = round(10 * sum / count)
    film.save()


@receiver(post_delete, sender=Rating)
def delete_rating(sender, instance, **kwargs):
    film = instance.film
    ratings = film.rating_set.all()
    sum = 0
    count = 0
    for rating in ratings:
        if not rating.profile.is_ratingban:
            sum += rating.rating
            count += 1
    if count == 0:
        film.average_rating = None
    else:
        film.average_rating = round(10 * sum / count)
    film.save()


@receiver(post_save, sender=Profile)
def ban_profile(sender, instance, created, **kwargs):
    profile_ratings = instance.rating_set.all()
    for profile_rating in profile_ratings:
        film = profile_rating.film
        ratings = film.rating_set.all()
        sum = 0
        count = 0
        for rating in ratings:
            if not rating.profile.is_ratingban:
                sum += rating.rating
                count += 1
        if count == 0:
            film.average_rating = None
        else:
            film.average_rating = round(10 * sum / count)
        film.save()


