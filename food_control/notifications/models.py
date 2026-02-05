import django.conf
import django.db.models


class Notification(django.db.models.Model):
    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        related_name="notifications",
        verbose_name="пользователь",
    )
    title = django.db.models.CharField(
        "заголовок",
        max_length=120,
    )
    message = django.db.models.TextField(
        "сообщение",
    )
    link = django.db.models.CharField(
        "ссылка",
        max_length=255,
        blank=True,
    )
    is_read = django.db.models.BooleanField(
        "прочитано",
        default=False,
    )
    created_at = django.db.models.DateTimeField(
        "создано",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user.email}: {self.title}"
