import django.conf
import django.db.models
import django.utils.timezone


class Meal(django.db.models.Model):
    class MealType(django.db.models.TextChoices):
        BREAKFAST = "breakfast", "Завтрак"
        LUNCH = "lunch", "Обед"

    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        related_name="meal",
        verbose_name="пользователь",
    )
    meal_type = django.db.models.CharField(
        "тип приёма пищи",
        max_length=20,
        choices=MealType.choices,
    )
    date = django.db.models.DateField(
        "дата",
        default=django.utils.timezone.now,
    )

    class Meta:
        verbose_name = "Приём пищи"
        verbose_name_plural = "Приёмы пищи"
        constraints = [
            django.db.models.UniqueConstraint(
                fields=["user", "meal_type", "date"],
                name="unique_meal_per_day",
            ),
        ]

    def __str__(self):
        return f"{self.user.email} — {self.meal_type} ({self.date})"
