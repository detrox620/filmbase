from django.db import models
from films.models import Country, MyModel
from django.contrib.auth.models import User


class Profile(MyModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Профиль оценок пользователя")

    is_ratingban = models.DateTimeField("Дата бана", blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Страна", null=True)

    class Meta:
        ordering = ["user"]
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.user.username
