from http import HTTPStatus

import django.test
from django.urls import reverse


class StaticURLTests(django.test.TestCase):
    def test_homepage_content(self):
        url = reverse("homepage:main")
        response = django.test.Client().get(url)
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
            f"Ожидался статус {HTTPStatus.OK}, но получен "
            "{response.status_code} для /",
        )
