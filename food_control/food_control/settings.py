from pathlib import Path

from food_control.utils import get_env


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = get_env(
    "DJANGO_SECRET_KEY",
    default="1234",
    cast=str,
)
DEBUG = get_env(
    "DJANGO_DEBUG",
    default=True,
    cast=bool,
)
ALLOWED_HOSTS = get_env(
    "DJANGO_ALLOWED_HOSTS",
    default=[
        "127.0.0.1",
        "localhost",
    ],
    cast=list,
)
ALLOW_REVERSE = get_env(
    "DJANGO_ALLOW_REVERSE",
    default=True,
    cast=bool,
)
DJANGO_MAIL = get_env(
    "DJANGO_MAIL",
    default="default@mysite.com",
    cast=str,
)

if DEBUG:
    DEFAULT_USER_IS_ACTIVE = get_env(
        "DJANGO_DEFAULT_USER_IS_ACTIVE",
        default=True,
        cast=bool,
    )
else:
    DEFAULT_USER_IS_ACTIVE = get_env(
        "DJANGO_DEFAULT_USER_IS_ACTIVE",
        default=False,
        cast=bool,
    )
    CSRF_TRUSTED_ORIGINS = get_env(
        "CSRF_TRUSTED_ORIGINS",
        default=[
            "http://127.0.0.1:8080",
            "http://localhost:8080",
            "http://nginx:80",
        ],
        cast=list,
    )

MAX_AUTH_ATTEMPTS = get_env(
    "DJANGO_MAX_AUTH_ATTEMPTS",
    default=10,
    cast=int,
)

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sorl.thumbnail",
    "tinymce",
    "core.apps.CoreConfig",
    "homepage.apps.HomepageConfig",
    "users.apps.UsersConfig",
    "django_cleanup.apps.CleanupConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "users.middleware.LoadUserMiddleware",
]

if DEBUG:
    INSTALLED_APPS.insert(-2, "debug_toolbar")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = ["127.0.0.1"]

ROOT_URLCONF = "food_control.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "food_control.wsgi.application"

if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        },
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": get_env(
                "POSTGRES_DB",
                default="food_control_db",
                cast=str,
            ),
            "USER": get_env("POSTGRES_USER", default="admin", cast=str),
            "PASSWORD": get_env(
                "POSTGRES_PASSWORD",
                default="password",
                cast=str,
            ),
            "HOST": get_env("POSTGRES_HOST", default="db", cast=str),
            "PORT": get_env("POSTGRES_PORT", default=5432, cast=int),
        },
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation"
            ".NumericPasswordValidator"
        ),
    },
]


LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static setup

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

STATICFILES_DIRS = [
    BASE_DIR / "static_dev",
]

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

# Auth setup

LOGIN_URL = "/users/login/"
LOGIN_REDIRECT_URL = "/users/profile/"
LOGOUT_REDIRECT_URL = "/users/login"

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = BASE_DIR / "send_mail"

else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

    EMAIL_HOST = get_env(
        "DJANGO_EMAIL_HOST",
        default="smtp.yandex.ru",
        cast=str,
    )
    EMAIL_PORT = get_env(
        "DJANGO_EMAIL_PORT",
        default=465,
        cast=int,
    )
    EMAIL_USE_SSL = get_env(
        "DJANGO_EMAIL_USE_SSL",
        default=True,
        cast=bool,
    )
    EMAIL_HOST_USER = get_env(
        "DJANGO_EMAIL_HOST_USER",
        default="",
        cast=str,
    )
    EMAIL_HOST_PASSWORD = get_env(
        "DJANGO_EMAIL_HOST_PASSWORD",
        default="",
        cast=str,
    )
    DEFAULT_FROM_EMAIL = get_env(
        "DJANGO_DEFAULT_FROM_EMAIL",
        default=EMAIL_HOST_USER,
        cast=str,
    )

AUTHENTICATION_BACKENDS = [
    "users.backends.AuthUserBackend",
]

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
