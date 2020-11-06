from django.db import models

from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel
from django_countries.fields import CountryField

class Cheese(TimeStampedModel):

    class Firmness(models.TextChoices):
        UNSPECIFIED = "unspecified", "Unspecified"
        SOFT = "soft", "Soft"
        SEMI_SOFT = "semi-soft", "Semi-Soft"
        SEMI_HARD = "semi-hard", "Semi-Hard"
        HARD = "hard", "Hard"

    name = models.CharField("Название сыра", max_length=255)
    slug = AutoSlugField("Адрес сыра",
                         unique=True, always_update=False, populate_from="name")
    description = models.TextField("Описание", blank=True)
    firmness = models.CharField("Твердость", max_length=20,
                                choices=Firmness.choices, default=Firmness.UNSPECIFIED)
    country_of_origin = CountryField("Страна происхождения", blank=True)

    def __str__(self):
        return self.name
