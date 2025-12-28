from datetime import timedelta
from http import HTTPStatus

import django.conf
import django.contrib.auth
import django.contrib.auth.mixins
import django.contrib.auth.views
import django.core.exceptions
import django.core.mail
import django.http
import django.shortcuts
import django.urls
import django.utils
import django.utils.timezone
import django.views.generic
import multi_form_view


import users.forms
import users.models


class SignUpView(django.views.generic.FormView):
    model = users.models.User
    form_class = users.forms.SignUpForm
    template_name = "users/signup.html"
    success_url = django.urls.reverse_lazy("users:login")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")

        user = form.save(commit=False)
        user.is_active = django.conf.settings.DEFAULT_USER_IS_ACTIVE
        user.save()
        users.models.Profile.objects.create(user=user)

        activation_url = self.request.build_absolute_uri(
            django.urls.reverse("users:activate", args=[user.username]),
        )

        form.save()
        django.core.mail.send_mail(
            "Активация профиля",
            activation_url,
            django.conf.settings.DJANGO_MAIL,
            [email],
            fail_silently=False,
        )
        return super().form_valid(form)


class ActivateView(django.views.generic.View):
    def get(self, request, username):
        user = django.shortcuts.get_object_or_404(
            users.models.User,
            username=username,
        )

        if user.is_active or (
            django.utils.timezone.now() - user.date_joined
        ) > timedelta(
            hours=12,
        ):
            return django.http.HttpResponse(status=HTTPStatus.NOT_FOUND)

        user.is_active = True
        user.save()
        return django.shortcuts.redirect("users:profile")


class ReactivateView(django.views.generic.View):
    def get(self, request, pk):
        user = django.shortcuts.get_object_or_404(users.models.User, pk=pk)

        if user.is_active or (
            django.utils.timezone.now() - user.profile.block_date
        ) > timedelta(
            days=7,
        ):
            return django.http.HttpResponse(status=HTTPStatus.NOT_FOUND)

        user.is_active = True
        user.save()
        return django.shortcuts.redirect("users:profile")


class UserListView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.ListView,
):
    template_name = "users/user_list.html"
    queryset = users.models.User.objects.filter(is_active=True)
    context_object_name = "users"


class UserDetailView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.DetailView,
):
    model = users.models.User
    template_name = "users/user_detail.html"
    context_object_name = "user"


class ProfileView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    multi_form_view.MultiModelFormView,
):
    form_classes = {
        "user_form": users.forms.UserChangeForm,
        "profile_form": users.forms.ProfileForm,
    }
    template_name = "users/profile.html"

    def get_objects(self):
        if self.request.user.profile.birthday:
            self.request.user.profile.birthday += timedelta(days=1)
            self.request.user.profile.birthday = (
                self.request.user.profile.birthday.strftime(
                    "%Y-%m-%d",
                )
            )

        return {
            "user_form": self.request.user,
            "profile_form": self.request.user.profile,
        }

    def get_success_url(self):
        return django.urls.reverse("users:profile")

    def forms_valid(self, forms):
        forms["user_form"].save()
        forms["profile_form"].save()

        return super(ProfileView, self).forms_valid(forms)


class CustomPasswordResetView(django.contrib.auth.views.PasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"

    def form_valid(self, form):
        email = form.cleaned_data.get("email")

        try:
            user = users.models.User.objects.by_mail(email)
        except users.models.User.DoesNotExist:
            user = None

        if not user:
            form.add_error(
                "email",
                django.core.exceptions.ValidationError(
                    "Пользователь с таким email не найден.",
                ),
            )
            return self.form_invalid(form)

        return super().form_valid(form)
