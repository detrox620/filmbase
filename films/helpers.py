from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CreateRatingForm
from .models import Rating


def paginate(request, collection, per=12):
    paginator = Paginator(collection, per)
    page = request.GET.get('page')
    try:
        collection = paginator.page(page)
    except PageNotAnInteger:
        collection = paginator.page(1)
    except EmptyPage:
        collection = paginator.page(paginator.num_pages)
    return collection


def build_rating_context(request, film):
    if not request.user.is_authenticated:
        return {
            'rating_form': None,
            'rating': None,
            'has_rating': False,
            'show_rating_form': False,
            'edit_mode': False,
        }

    profile = request.user.profile
    existing_rating = Rating.objects.filter(film=film, profile=profile).first()
    edit_mode = request.GET.get('edit') == '1'

    if edit_mode:
        form = CreateRatingForm(
            initial={'rating': existing_rating.rating if existing_rating else 5}
        )
        return {
            'rating_form': form,
            'rating': existing_rating.rating if existing_rating else None,
            'has_rating': bool(existing_rating),
            'show_rating_form': False,
            'edit_mode': True,
        }
    elif existing_rating:
        return {
            'rating_form': None,
            'rating': existing_rating.rating,
            'has_rating': True,
            'show_rating_form': False,
            'edit_mode': False,
        }
    else:
        return {
            'rating_form': CreateRatingForm(),
            'rating': None,
            'has_rating': False,
            'show_rating_form': True,
            'edit_mode': False,
        }


def calculate_average_rating(film, form):
    if form.is_valid():
        country = form.cleaned_data['country']
        time_start = form.cleaned_data['time_start']
        time_end = form.cleaned_data['time_end']
        ratings = film.rating_set.all()
        sum = 0
        count = 0
        for rating in ratings:
            condition = ((country == rating.profile.country or country is None)
                         and ((time_start is None and time_end is None)
                         or (time_start <= rating.updated_at <= time_end))
                         and not rating.profile.is_ratingban)
            if condition:
                sum += rating.rating
                count += 1
        if count == 0:
            average_rating = None
        else:
            average_rating = sum / count
        return average_rating
