import uuid

import django.conf
import django.db.models


class FoodAccess(django.db.models.Model):
    user = django.db.models.OneToOneField(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        related_name="food_access",
        verbose_name="пользователь",
    )
    meals_left = django.db.models.PositiveIntegerField(
        "доступных приёмов пищи",
        default=0,
    )
    is_active = django.db.models.BooleanField(
        "активен",
        default=False,
    )

    class Meta:
        verbose_name = "Доступ к питанию"
        verbose_name_plural = "Доступы к питанию"

    def __str__(self):
        return f"{self.user.email}: {self.meals_left}"


class Payment(django.db.models.Model):
    class PaymentType(django.db.models.TextChoices):
        SINGLE = "single", "Разовый платёж"
        SUBSCRIPTION = "subscription", "Абонемент"

    MEALS_MAP = {
        PaymentType.SINGLE: 1,
        PaymentType.SUBSCRIPTION: 20,
    }

    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        related_name="payments",
        verbose_name="пользователь",
    )
    payment_type = django.db.models.CharField(
        "тип оплаты",
        max_length=20,
        choices=PaymentType.choices,
    )
    amount = django.db.models.PositiveIntegerField(
        "сумма",
    )
    created = django.db.models.DateTimeField(
        "дата оплаты",
        auto_now_add=True,
    )
    is_success = django.db.models.BooleanField(
        "успешно",
        default=True,  # заглушка
    )
    idempotency_key = django.db.models.UUIDField(
        "уникальный код",
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"
        ordering = ("-created",)

    def __str__(self):
        return f"{self.user.email} - {self.amount}₽"
