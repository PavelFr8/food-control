from http import HTTPStatus

from django.contrib.auth import get_user_model
import django.contrib.auth.tokens
from django.core import mail
from django.test import override_settings, TestCase
import django.urls
import django.utils.encoding
import django.utils.http


User = get_user_model()


class UserSignupTests(TestCase):
    fixtures = ["fixtures/roles.json"]

    @override_settings(DEFAULT_USER_IS_ACTIVE=True)
    def test_signup_active_user(self):
        form_data = {
            "email": "test@test.com",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "last_name": "Иванов",
            "first_name": "Иван",
            "patronymic": "Иванович",
            "birthday": "2000-01-01",
            "school_class": 10,
        }

        response = self.client.post(
            django.urls.reverse("users:signup"),
            data=form_data,
        )

        self.assertRedirects(
            response,
            django.urls.reverse("users:login"),
        )

        user = User.objects.get(email="test@test.com")
        self.assertTrue(user.is_active)

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Активация профиля", mail.outbox[0].subject)
        self.assertIn("activate", mail.outbox[0].body)

    @override_settings(DEFAULT_USER_IS_ACTIVE=False)
    def test_signup_inactive_user(self):
        form_data = {
            "email": "test@test.com",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "last_name": "Иванов",
            "first_name": "Иван",
            "patronymic": "Иванович",
            "birthday": "2000-01-01",
            "school_class": 10,
        }

        response = self.client.post(
            django.urls.reverse("users:signup"),
            data=form_data,
        )

        self.assertRedirects(
            response,
            django.urls.reverse("users:login"),
        )

        user = User.objects.get(email="test@test.com")
        self.assertFalse(user.is_active)

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Активация профиля", mail.outbox[0].subject)
        self.assertIn("activate", mail.outbox[0].body)

    def test_signup_invalid_form(self):
        form_data = {
            "email": "invalid-email",
            "password1": "short",
            "password2": "mismatch",
        }

        response = self.client.post(
            django.urls.reverse("users:signup"),
            data=form_data,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(User.objects.exists())


class UserActivationTests(TestCase):
    fixtures = ["fixtures/roles.json"]

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="StrongPass123",
            is_active=False,
        )

        self.uidb64 = django.utils.http.urlsafe_base64_encode(
            django.utils.encoding.force_bytes(self.user.pk),
        )
        self.token = (
            django.contrib.auth.tokens.default_token_generator.make_token(
                self.user,
            )
        )

        self.activation_url = django.urls.reverse(
            "users:activate",
            kwargs={
                "uidb64": self.uidb64,
                "token": self.token,
            },
        )

    def test_activate_user_success(self):
        response = self.client.get(self.activation_url, follow=True)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_activate_user_invalid_token(self):
        bad_url = django.urls.reverse(
            "users:activate",
            kwargs={
                "uidb64": self.uidb64,
                "token": "invalid-token",
            },
        )

        response = self.client.get(bad_url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_activate_user_already_active(self):
        self.user.is_active = True
        self.user.save()

        response = self.client.get(self.activation_url)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
