from http import HTTPStatus

import django.contrib.auth
import django.core.exceptions
import django.test
import django.urls

import menu.forms
import menu.models


User = django.contrib.auth.get_user_model()


class MenuModelsFormsViewsTests(django.test.TestCase):
    fixtures = ["fixtures/roles.json", "fixtures/menu.json"]

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com",
            password="StrongPass123",
        )

        self.dish = menu.models.Dish.objects.get(pk=1)

    def test_dish_features_name_normalization(self):
        feature = menu.models.DishFeatures.objects.create(
            name="  БЕЗ САХАРА  ",
        )
        self.assertEqual(feature.name, "Без сахара")

    def test_dish_str_capitalized(self):
        self.assertEqual(str(self.dish), "Чай")

    def test_ingredient_clean_rejects_digits(self):
        ingredient = menu.models.Ingredient(
            dish=self.dish,
            name="Молоко2",
            quantity=100,
            unit="мл",
        )

        with self.assertRaises(django.core.exceptions.ValidationError) as ctx:
            ingredient.full_clean()

        self.assertIn("name", ctx.exception.message_dict)

    def test_ingredient_clean_rejects_invalid_quantity(self):
        ingredient = menu.models.Ingredient(
            dish=self.dish,
            name="Вода",
            quantity=0,
            unit="мл",
        )

        with self.assertRaises(django.core.exceptions.ValidationError) as ctx:
            ingredient.full_clean()

        self.assertIn("quantity", ctx.exception.message_dict)

    def test_valid_ingredient_passes_clean(self):
        ingredient = menu.models.Ingredient(
            dish=self.dish,
            name="Вода",
            quantity=200,
            unit="мл",
        )

        ingredient.full_clean()

    def test_breakfast_and_lunch_str(self):
        self.assertEqual(str(menu.models.BreakfastMenu()), "Завтрак")
        self.assertEqual(str(menu.models.LunchMenu()), "Обед")

    def test_breakfast_menu_form_valid(self):
        form = menu.forms.BreakfastMenuForm(
            data={"drink1": self.dish.pk},
        )
        self.assertTrue(form.is_valid())

    def test_lunch_menu_form_valid(self):
        form = menu.forms.LunchMenuForm(
            data={"soup1": self.dish.pk},
        )
        self.assertTrue(form.is_valid())

    def test_all_form_widgets_have_bootstrap_class(self):
        breakfast_form = menu.forms.BreakfastMenuForm()
        lunch_form = menu.forms.LunchMenuForm()

        for form in (breakfast_form, lunch_form):
            for field in form.fields.values():
                self.assertEqual(
                    field.widget.attrs.get("class"),
                    "form-select",
                )

    def test_menu_view_login_required(self):
        url = django.urls.reverse("menu:menu")
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_menu_view_success(self):
        self.client.login(
            email="user@test.com",
            password="StrongPass123",
        )

        url = django.urls.reverse("menu:menu")
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("breakfast", response.context)
        self.assertIn("lunch", response.context)

    def test_dish_detail_view_login_required(self):
        url = django.urls.reverse(
            "menu:dish_detail",
            kwargs={"pk": self.dish.pk},
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_dish_detail_view_success(self):
        self.client.force_login(self.user)

        url = django.urls.reverse(
            "menu:dish_detail",
            kwargs={"pk": self.dish.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["dish"], self.dish)

    def test_edit_breakfast_menu_get_creates_object(self):
        url = django.urls.reverse("menu:edit_breakfast")
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(
            menu.models.BreakfastMenu.objects.filter(pk=1).exists(),
        )

    def test_edit_breakfast_menu_post_updates_object(self):
        url = django.urls.reverse("menu:edit_breakfast")
        self.client.post(url, data={"drink1": self.dish.pk})

        breakfast = menu.models.BreakfastMenu.objects.get(pk=1)
        self.assertEqual(breakfast.drink1, self.dish)

    def test_edit_lunch_menu_get_creates_object(self):
        url = django.urls.reverse("menu:edit_lunch")
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(
            menu.models.LunchMenu.objects.filter(pk=1).exists(),
        )

    def test_edit_lunch_menu_post_updates_object(self):
        url = django.urls.reverse("menu:edit_lunch")
        self.client.post(url, data={"salad1": self.dish.pk})

        lunch = menu.models.LunchMenu.objects.get(pk=1)
        self.assertEqual(lunch.salad1, self.dish)
