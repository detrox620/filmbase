from django import forms
from dal import autocomplete
from .models import Country, Genre, Film, Person


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name']


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['name', 'origin_name', 'slogan', 'length', 'year',
                  'trailer_url', 'cover', 'description', 'country', 'genres',
                  "director", 'people']
        widgets = {
            'people': autocomplete.ModelSelect2Multiple(
                url='films:person_autocomplete'),
            'director': autocomplete.ModelSelect2(
                url='films:person_autocomplete'),
            'country': autocomplete.ModelSelect2(
                url='films:country_autocomplete'),
        }


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'origin_name', 'birthday', 'photo']
        widgets = {
            "birthday": forms.DateInput(attrs={'type': 'date'},
                                        format="%Y-%m-%d")
        }


class CreateRatingForm(forms.Form):
    rating = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 11)])


class FilterRatingForm(forms.Form):
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        empty_label="Выберите страну",
        required=False)
    time_start = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        required=False)
    time_end = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        required=False)


ORDER_CHOICES = [
    ('name', 'По названию (А-Я)'),
    ('-name', 'По названию (Я-А)'),
    ('-average_rating', 'По рейтингу (убывание)'),
    ('average_rating', 'По рейтингу (возрастание)'),
]


class FilterFilmsForm(forms.Form):
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        empty_label="Выберите страну",
        required=False)
    genres = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        empty_label="Выберите жанр",
        required=False)

    choices = [(round(i * 0.1, 1), f"{round(i * 0.1, 1):.1f}") for i in range(10, 101)]
    rating_start = forms.ChoiceField(choices=choices, initial='1.0')
    rating_end = forms.ChoiceField(choices=choices, initial='10.0')
    query = forms.CharField(required=False)
    order_by = forms.ChoiceField(choices=ORDER_CHOICES, required=False, initial='name')