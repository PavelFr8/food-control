import sys

import django.contrib.auth.models as auth_models
import django.db.models
from sorl.thumbnail import get_thumbnail

import users.validators


class UserManager(auth_models.UserManager):
    DOMAINS = {
        "ya.ru": "yandex.ru",
    }
    SYMBOLS = {
        "yandex.ru": "-",
        "gmail.com": "",
    }

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                auth_models.User.profile.related.name,
            )
        )

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def by_mail(self, mail):
        mail = self.normalize_email(mail)
        return self.active().get(email=mail)

    @classmethod
    def normalize_email(cls, email):
        email = super().normalize_email(email).lower()
        try:
            email_name, domain = email.strip().rsplit("@", 1)
            email_name, _ = email_name.split("+", 1)
            domain = cls.DOMAINS.get(domain, domain)

            email_name = email_name.replace(
                ".",
                cls.SYMBOLS.get(domain, "."),
            )
        except ValueError:
            pass
        else:
            email = "@".join(email_name, domain.lower())

        return email


class User(auth_models.User):
    objects = UserManager()

    class Meta:
        proxy = True


class Profile(django.db.models.Model):
    def image_path(self, filename):
        return f"users/{self.user.id}/{filename}"

    user = django.db.models.OneToOneField(
        auth_models.User,
        on_delete=django.db.models.CASCADE,
        related_name="profile",
        null=True,
    )
    birthday = django.db.models.DateTimeField(
        "дата рождения",
        blank=True,
        null=True,
        validators=[users.validators.validate_not_future],
    )
    image = django.db.models.ImageField(
        "аватар",
        blank=True,
        null=True,
        upload_to=image_path,
    )
    attempts_count = django.db.models.PositiveIntegerField(
        "попытки входа",
        default=0,
    )
    block_date = django.db.models.DateTimeField(
        "дата блокировки",
        blank=True,
        null=True,
    )

    def get_image(self):
        return get_thumbnail(self.image, "200x200", crop="center", quality=51)

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили"


if "makemigrations" not in sys.argv and "migrate" not in sys.argv:
    auth_models.User._meta.get_field("email")._unique = True
