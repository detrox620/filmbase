from django import forms
from films.models import Country


class ChangeCountryForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Выберите страну", label='Страна')