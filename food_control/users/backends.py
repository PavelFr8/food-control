import django.conf
import django.contrib.auth.backends
import django.urls
import django.utils.timezone


import users.models


class AuthUserBackend(django.contrib.auth.backends.ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = users.models.User.objects.by_mail(username)
        except users.models.User.DoesNotExist:
            return None

        if user.check_password(password):
            user.attempts_count = 0
            user.save()
            return user

        user.attempts_count += 1
        if user.attempts_count >= django.conf.settings.MAX_AUTH_ATTEMPTS:
            user.is_active = False
            user.block_date = django.utils.timezone.now()
            user.save()
            reactivate_url = request.build_absolute_uri(
                django.urls.reverse(
                    "users:reactivate",
                    kwargs={"pk": user.id},
                ),
            )
            django.core.mail.send_mail(
                "Слишком много попыток входа! Аккаунт заблокирован!",
                f"Но вот ссылка на восстановление {reactivate_url}",
                django.conf.settings.DJANGO_MAIL,
                [user.email],
                fail_silently=False,
            )

        return None
