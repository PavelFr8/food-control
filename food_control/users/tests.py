from datetime import timedelta
from http import HTTPStatus
from unittest import mock

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings, TestCase
from django.urls import reverse


User = get_user_model()


class UserSignupTests(TestCase):
    @override_settings(DEFAULT_USER_IS_ACTIVE=True)
    def test_signup_form_valid_debug_true(self):
        form_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
        }
        response = self.client.post(
            reverse("users:signup"),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, reverse("users:login"))
        self.assertTrue(User.objects.filter(username="testuser").exists())
        user = User.objects.get(username="testuser")
        self.assertTrue(user.is_active)
        self.assertEqual(user.email, "test@test.com")

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Активация профиля", mail.outbox[0].subject)
        self.assertIn(user.username, mail.outbox[0].body)

    @override_settings(DEFAULT_USER_IS_ACTIVE=False)
    def test_signup_form_valid_debug_false(self):
        form_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
        }
        response = self.client.post(
            reverse("users:signup"),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, reverse("users:login"))
        self.assertTrue(User.objects.filter(username="testuser").exists())
        user = User.objects.get(username="testuser")
        self.assertFalse(user.is_active)
        self.assertEqual(user.email, "test@test.com")

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Активация профиля", mail.outbox[0].subject)
        self.assertIn(user.username, mail.outbox[0].body)

    def test_signup_form_invalid(self):
        form_data = {
            "username": "",
            "email": "invalid-email",
            "password1": "short",
            "password2": "mismatch",
        }
        response = self.client.post(reverse("users:signup"), data=form_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(User.objects.exists())


class UserActivationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPass123",
            is_active=False,
        )
        self.activation_url = reverse(
            "users:activate",
            args=[self.user.username],
        )

    def test_activate_user_success(self):
        self.client.get(self.activation_url, follow=True)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    @mock.patch("django.utils.timezone.now")
    def test_activate_user_expired(self, mock_now):
        mock_now.return_value = self.user.date_joined + timedelta(hours=13)
        response = self.client.get(self.activation_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_activate_user_already_active(self):
        self.user.is_active = True
        self.user.save()
        response = self.client.get(self.activation_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
