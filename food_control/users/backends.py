import django.conf
import django.contrib.auth.backends
import django.contrib.auth.models as auth_models
import django.urls
import django.utils.timezone


import users.models


class AuthUserBackend(django.contrib.auth.backends.ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if "@" in username:
                user = users.models.User.objects.by_mail(username)
            else:
                user = users.models.User.objects.get(username=username)
        except users.models.User.DoesNotExist:
            return None

        if user.check_password(password):
            try:
                user.profile
            except auth_models.User.profile.RelatedObjectDoesNotExist:
                users.models.Profile.objects.create(user=user)

            user.profile.attempts_count = 0
            user.profile.save()

            return user

        user.profile.attempts_count += 1
        if (
            user.profile.attempts_count
            >= django.conf.settings.MAX_AUTH_ATTEMPTS
        ):
            user.is_active = False
            user.profile.block_date = django.utils.timezone.now()
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

        user.profile.save()

        return None
