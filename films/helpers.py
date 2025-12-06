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


def build_rating_ui_context(request, film):
    if not request.user.is_authenticated:
        return {
            'form': None,
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
            'form': form,
            'rating': existing_rating.rating if existing_rating else None,
            'has_rating': bool(existing_rating),
            'show_rating_form': False,
            'edit_mode': True,
        }
    elif existing_rating:
        return {
            'form': None,
            'rating': existing_rating.rating,
            'has_rating': True,
            'show_rating_form': False,
            'edit_mode': False,
        }
    else:
        return {
            'form': CreateRatingForm(),
            'rating': None,
            'has_rating': False,
            'show_rating_form': True,
            'edit_mode': False,
        }



