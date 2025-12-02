from django.contrib.auth import login, authenticate
from .forms import Form
from django.shortcuts import render, redirect
from films.models import Profile, Country


def signup(request):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            country = form.cleaned_data.get('country')

            user = authenticate(username=username, password=raw_password)
            login(request, user)

            rating_user, created = Profile.objects.get_or_create(user=user)
            rating_user.country = country
            rating_user.save()

            return redirect('films:home')
    else:
        form = Form()
    return render(request, "signup/signup.html", {'form': form})
