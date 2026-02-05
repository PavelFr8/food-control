import django.conf
import django.db.models


class StockItem(django.db.models.Model):
    class UnitChoice(django.db.models.TextChoices):
        GRAM = "г", "г"
        ML = "мл", "мл"
        PIECE = "шт", "шт"

    name = django.db.models.CharField(
        "продукт",
        max_length=100,
        unique=True,
    )
    unit = django.db.models.CharField(
        "единица",
        max_length=10,
        choices=UnitChoice.choices,
    )
    quantity = django.db.models.PositiveIntegerField(
        "остаток",
        default=0,
    )
    updated_at = django.db.models.DateTimeField(
        "обновлено",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Остаток"
        verbose_name_plural = "Остатки"
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"


class ProcurementRequest(django.db.models.Model):
    class StatusChoice(django.db.models.TextChoices):
        PENDING = "pending", "На согласовании"
        APPROVED = "approved", "Согласовано"
        REJECTED = "rejected", "Отклонено"

    item_name = django.db.models.CharField(
        "наименование",
        max_length=100,
    )
    unit = django.db.models.CharField(
        "единица",
        max_length=10,
        choices=StockItem.UnitChoice.choices,
    )
    quantity = django.db.models.PositiveIntegerField(
        "количество",
    )
    status = django.db.models.CharField(
        "статус",
        max_length=20,
        choices=StatusChoice.choices,
        default=StatusChoice.PENDING,
    )
    comment = django.db.models.TextField(
        "комментарий",
        blank=True,
    )
    created_by = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        related_name="procurement_requests",
        verbose_name="создал",
    )
    reviewed_by = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.SET_NULL,
        related_name="reviewed_procurements",
        verbose_name="согласовал",
        null=True,
        blank=True,
    )
    created_at = django.db.models.DateTimeField(
        "создано",
        auto_now_add=True,
    )
    reviewed_at = django.db.models.DateTimeField(
        "согласовано",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Заявка на закупку"
        verbose_name_plural = "Заявки на закупку"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.item_name} — {self.quantity} {self.unit}"
