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
            name="Notification",
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
                    "title",
                    django.db.models.CharField(
                        max_length=120,
                        verbose_name="заголовок",
                    ),
                ),
                (
                    "message",
                    django.db.models.TextField(
                        verbose_name="сообщение",
                    ),
                ),
                (
                    "link",
                    django.db.models.CharField(
                        blank=True,
                        max_length=255,
                        verbose_name="ссылка",
                    ),
                ),
                (
                    "is_read",
                    django.db.models.BooleanField(
                        default=False,
                        verbose_name="прочитано",
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
                    "user",
                    django.db.models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications",
                        to=django.conf.settings.AUTH_USER_MODEL,
                        verbose_name="пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Уведомление",
                "verbose_name_plural": "Уведомления",
                "ordering": ("-created_at",),
            },
        ),
    ]
