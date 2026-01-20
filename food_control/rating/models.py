import django.db.models

import menu.models


class Rating(django.db.models.Model):
    class MarkChoice(django.db.models.IntegerChoices):
        HATE = 1, "Ненависть"
        DISLIKE = 2, "Неприязнь"
        NEUTRAL = 3, "Нейтрально"
        ADORATION = 4, "Обожание"
        LOVE = 5, "Любовь"

    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        verbose_name="пользователь",
    )
    dish = django.db.models.ForeignKey(
        menu.models.Dish,
        on_delete=django.db.models.CASCADE,
        verbose_name="блюдо",
    )
    mark = django.db.models.PositiveSmallIntegerField(
        choices=MarkChoice.choices,
        null=False,
        verbose_name="оценка",
    )
    comment = django.db.models.TextField(
        null=False,
        verbose_name="комментарий",
    )
    created = django.db.models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата создания",
        null=True,
    )

    class Meta:
        default_related_name = "ratings"
        verbose_name = "рейтинг"
        verbose_name_plural = "рейтинги"
        unique_together = ["user", "dish"]
