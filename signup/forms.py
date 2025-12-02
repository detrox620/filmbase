from django.contrib.auth.forms import UserCreationForm
from django import forms
from films.models import Country


class Form(UserCreationForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Выберите страну")