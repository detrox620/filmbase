from django.shortcuts import render, redirect
from .forms import ChangeCountryForm


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    username = user.username
    profile = user.profile
    country = profile.country
    number_ratings = profile.rating_set.count()


    if request.method == 'POST':
        form = ChangeCountryForm(request.POST)
        if form.is_valid():
            new_country = form.cleaned_data['country']
            profile.country = new_country
            profile.save()
            return redirect('profiles:profile')
    else:
        form = ChangeCountryForm(initial={'country': profile.country})

    context = {'username': username, 'country': country, 'number_ratings': number_ratings, 'form': form}
    return render(request, 'profiles/profile.html', context)