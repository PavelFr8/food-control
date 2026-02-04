import django.contrib.auth.models as auth_models
import django.db.models

import users.validators


class UserManager(auth_models.BaseUserManager):
    DOMAINS = {
        "ya.ru": "yandex.ru",
    }
    SYMBOLS = {
        "yandex.ru": "-",
        "gmail.com": "",
    }

    def get_queryset(self):
        return super().get_queryset().select_related("role")

    def get_students(self):
        return self.get_queryset().filter(role__name="student")

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def by_mail(self, mail):
        mail = self.normalize_email(mail)
        return self.active().get(email=mail)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

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


class FoodFeatures(django.db.models.Model):
    name = django.db.models.CharField(
        "пищевая особенность",
        max_length=64,
    )

    class Meta:
        verbose_name = "Пищевая особенность"
        verbose_name_plural = "Пищевые особенности"

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip().lower().capitalize()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Role(django.db.models.Model):
    class RoleNames(django.db.models.TextChoices):
        STUDENT = "student", "ученик"
        COOK = "cook", "повар"
        ADMIN = "admin", "администратор"

    name = django.db.models.CharField(
        "название",
        choices=RoleNames.choices,
        unique=True,
        default=RoleNames.STUDENT,
    )

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

    def __str__(self):
        return self.name


class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = django.db.models.EmailField(
        "email",
        unique=True,
        db_index=True,
    )
    is_active = django.db.models.BooleanField(
        "активен",
        default=True,
    )
    is_staff = django.db.models.BooleanField(
        "персонал",
        default=False,
    )
    date_joined = django.db.models.DateTimeField(
        "дата регистрации",
        default=django.utils.timezone.now,
    )

    class SchoolClass(django.db.models.IntegerChoices):
        CLASS_1 = 1, "1 класс"
        CLASS_2 = 2, "2 класс"
        CLASS_3 = 3, "3 класс"
        CLASS_4 = 4, "4 класс"
        CLASS_5 = 5, "5 класс"
        CLASS_6 = 6, "6 класс"
        CLASS_7 = 7, "7 класс"
        CLASS_8 = 8, "8 класс"
        CLASS_9 = 9, "9 класс"
        CLASS_10 = 10, "10 класс"
        CLASS_11 = 11, "11 класс"

    last_name = django.db.models.CharField(
        "фамилия",
        max_length=50,
        validators=[users.validators.fio_validator],
    )

    first_name = django.db.models.CharField(
        "имя",
        max_length=50,
        validators=[users.validators.fio_validator],
    )

    patronymic = django.db.models.CharField(
        "отчество",
        max_length=50,
        blank=True,
        null=True,
        validators=[users.validators.fio_validator],
    )

    role = django.db.models.ForeignKey(
        Role,
        on_delete=django.db.models.PROTECT,
        default=1,
        verbose_name="роль",
    )

    school_class = django.db.models.IntegerField(
        "класс в школе",
        choices=SchoolClass.choices,
        blank=True,
        null=True,
    )

    food_features = django.db.models.ManyToManyField(
        FoodFeatures,
        blank=True,
        verbose_name="индивидуальные предпочтения",
    )

    birthday = django.db.models.DateTimeField(
        "дата рождения",
        blank=True,
        null=True,
        validators=[users.validators.validate_not_future],
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

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    groups = django.db.models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True,
        help_text="Группы, к которым принадлежит пользователь.",
        verbose_name="группы",
    )

    user_permissions = django.db.models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_set_permissions",
        blank=True,
        help_text="Специальные разрешения для пользователя.",
        verbose_name="разрешения пользователя",
    )

    def save(self, *args, **kwargs):
        self.last_name = self.last_name.strip().lower().capitalize()
        self.first_name = self.first_name.strip().lower().capitalize()
        if self.patronymic:
            self.patronymic = self.patronymic.strip().lower().capitalize()

        super().save(*args, **kwargs)
