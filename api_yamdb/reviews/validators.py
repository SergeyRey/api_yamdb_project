from django.db import models
from django.utils import timezone


def validate_year(value):

    year = timezone.now().year
    if value > year:
        raise models.ValidationError(
            'Проверьте год издания произведения!'
        )
    return value
