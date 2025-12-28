import datetime

import django.core.exceptions
import django.utils.timezone


def validate_not_future(value):
    if value:
        if value > django.utils.timezone.now():
            raise django.core.exceptions.ValidationError(
                "Ого! Вы что из будущего?",
            )

        if value < django.utils.timezone.now() - datetime.timedelta(
            days=365 * 120,
        ):

            raise django.core.exceptions.ValidationError(
                "Ого! Вы что из прошлого?",
            )
