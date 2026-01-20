from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

from menu.models import Dish
from rating.forms import RatingForm
from rating.models import Rating


User = get_user_model()


class RatingModelTests(TestCase):
    fixtures = ["fixtures/roles.json", "fixtures/menu.json"]

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            password="StrongPass123",
        )
        self.dish = Dish.objects.get(pk=1)

    def test_create_rating_success(self):
        rating = Rating.objects.create(
            user=self.user,
            dish=self.dish,
            mark=Rating.MarkChoice.LOVE,
            comment="Очень вкусно",
        )

        self.assertEqual(rating.user, self.user)
        self.assertEqual(rating.dish, self.dish)
        self.assertEqual(rating.mark, Rating.MarkChoice.LOVE)
        self.assertEqual(rating.comment, "Очень вкусно")

    def test_unique_user_dish_constraint(self):
        Rating.objects.create(
            user=self.user,
            dish=self.dish,
            mark=Rating.MarkChoice.NEUTRAL,
            comment="Норм",
        )

        with self.assertRaises(IntegrityError):
            Rating.objects.create(
                user=self.user,
                dish=self.dish,
                mark=Rating.MarkChoice.LOVE,
                comment="Еще раз",
            )


class RatingFormTests(TestCase):
    def test_form_valid_data(self):
        form = RatingForm(
            data={
                "mark": Rating.MarkChoice.LOVE,
                "comment": "Очень понравилось",
            },
        )

        self.assertTrue(form.is_valid())

    def test_form_empty_data(self):
        form = RatingForm(data={})

        self.assertFalse(form.is_valid())
        self.assertIn("mark", form.errors)
        self.assertIn("comment", form.errors)

    def test_mark_choices_present(self):
        form = RatingForm()

        self.assertEqual(
            form.fields["mark"].choices,
            Rating.MarkChoice.choices,
        )
