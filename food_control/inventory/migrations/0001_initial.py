import django.conf
import django.db.models
import django.db.models.deletion
from django.db import migrations


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(django.conf.settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="StockItem",
            fields=[
                (
                    "id",
                    django.db.models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    django.db.models.CharField(
                        max_length=100,
                        unique=True,
                        verbose_name="продукт",
                    ),
                ),
                (
                    "unit",
                    django.db.models.CharField(
                        choices=[("г", "г"), ("мл", "мл"), ("шт", "шт")],
                        max_length=10,
                        verbose_name="единица",
                    ),
                ),
                (
                    "quantity",
                    django.db.models.PositiveIntegerField(
                        default=0,
                        verbose_name="остаток",
                    ),
                ),
                (
                    "updated_at",
                    django.db.models.DateTimeField(
                        auto_now=True,
                        verbose_name="обновлено",
                    ),
                ),
            ],
            options={
                "verbose_name": "Остаток",
                "verbose_name_plural": "Остатки",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="ProcurementRequest",
            fields=[
                (
                    "id",
                    django.db.models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "item_name",
                    django.db.models.CharField(
                        max_length=100,
                        verbose_name="наименование",
                    ),
                ),
                (
                    "unit",
                    django.db.models.CharField(
                        choices=[("г", "г"), ("мл", "мл"), ("шт", "шт")],
                        max_length=10,
                        verbose_name="единица",
                    ),
                ),
                (
                    "quantity",
                    django.db.models.PositiveIntegerField(
                        verbose_name="количество",
                    ),
                ),
                (
                    "status",
                    django.db.models.CharField(
                        choices=[
                            ("pending", "На согласовании"),
                            ("approved", "Согласовано"),
                            ("rejected", "Отклонено"),
                        ],
                        default="pending",
                        max_length=20,
                        verbose_name="статус",
                    ),
                ),
                (
                    "comment",
                    django.db.models.TextField(
                        blank=True,
                        verbose_name="комментарий",
                    ),
                ),
                (
                    "created_at",
                    django.db.models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="создано",
                    ),
                ),
                (
                    "reviewed_at",
                    django.db.models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name="согласовано",
                    ),
                ),
                (
                    "created_by",
                    django.db.models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="procurement_requests",
                        to=django.conf.settings.AUTH_USER_MODEL,
                        verbose_name="создал",
                    ),
                ),
                (
                    "reviewed_by",
                    django.db.models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="reviewed_procurements",
                        to=django.conf.settings.AUTH_USER_MODEL,
                        verbose_name="согласовал",
                    ),
                ),
            ],
            options={
                "verbose_name": "Заявка на закупку",
                "verbose_name_plural": "Заявки на закупку",
                "ordering": ("-created_at",),
            },
        ),
    ]
