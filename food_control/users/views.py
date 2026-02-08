from datetime import timedelta
from http import HTTPStatus

import django.conf
import django.contrib.auth
import django.contrib.auth.mixins
import django.contrib.auth.tokens
import django.contrib.auth.views
import django.core.exceptions
import django.core.mail
import django.http
import django.shortcuts
import django.urls
import django.utils
import django.utils.timezone
import django.views.generic

import meals.models
import users.forms
import users.models


class SignUpView(django.views.generic.FormView):
    model = users.models.User
    form_class = users.forms.SignUpForm
    template_name = "users/signup.html"
    success_url = django.urls.reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = django.conf.settings.DEFAULT_USER_IS_ACTIVE
        user.save()

        uidb64 = django.utils.http.urlsafe_base64_encode(
            django.utils.encoding.force_bytes(user.pk),
        )
        token = django.contrib.auth.tokens.default_token_generator.make_token(
            user,
        )

        activation_path = django.urls.reverse(
            "users:activate",
            kwargs={"uidb64": uidb64, "token": token},
        )
        activation_url = f"{django.conf.settings.BASE_URL}{activation_path}"
        django.core.mail.send_mail(
            "Активация профиля",
            activation_url,
            django.conf.settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return super().form_valid(form)


class ActivateView(django.views.generic.View):
    def get(self, request, uidb64, token):
        try:
            uid = int(django.utils.http.urlsafe_base64_decode(uidb64).decode())
            user = django.shortcuts.get_object_or_404(
                users.models.User,
                pk=uid,
            )
        except (
            TypeError,
            ValueError,
            OverflowError,
            users.models.User.DoesNotExist,
        ):
            return django.http.HttpResponse(status=HTTPStatus.NOT_FOUND)

        if (
            not django.contrib.auth.tokens.default_token_generator.check_token(
                user,
                token,
            )
            or user.is_active
        ):
            return django.http.HttpResponse(status=HTTPStatus.NOT_FOUND)

        user.is_active = True
        user.save()

        profile_path = django.urls.reverse("users:profile")
        return django.shortcuts.redirect(
            f"{django.conf.settings.BASE_URL}{profile_path}",
        )


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

        profile_path = django.urls.reverse("users:profile")
        return django.shortcuts.redirect(
            f"{django.conf.settings.BASE_URL}{profile_path}",
        )


class UserDetailView(
    users.forms.RoleRequiredMixin,
    django.views.generic.DetailView,
):
    required_roles = [
        users.models.Role.RoleNames.COOK,
    ]
    model = users.models.User
    template_name = "users/user_detail.html"
    context_object_name = "detail_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        today = django.utils.timezone.now().date()

        access = getattr(user, "food_access", None)

        has_access = bool(
            access and access.is_active and access.meals_left > 0,
        )

        meals_today = set(
            meals.models.Meal.objects.filter(
                user=user,
                date=today,
            ).values_list("meal_type", flat=True),
        )

        context.update(
            {
                "has_food_access": has_access,
                "meals_today": meals_today,
            },
        )
        return context


class UserView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.UpdateView,
):
    model = users.models.User
    form_class = users.forms.UserFoodFeaturesForm
    template_name = "users/profile.html"
    success_url = django.urls.reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.role.name == users.models.Role.RoleNames.STUDENT:
            today = django.utils.timezone.now().date()
            access = getattr(user, "food_access", None)
            context["has_food_access"] = bool(
                access and access.is_active and access.meals_left > 0,
            )
            context["meals_today"] = set(
                meals.models.Meal.objects.filter(
                    user=user,
                    date=today,
                ).values_list("meal_type", flat=True),
            )

        return context


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

        self.extra_email_context = {
            "base_url": django.conf.settings.BASE_URL,
        }

        return super().form_valid(form)
