import re

import django.core.exceptions
import django.db.models


class DishFeatures(django.db.models.Model):
    name = django.db.models.CharField(
        "особенность",
        max_length=64,
    )

    class Meta:
        verbose_name = "Особенность блюда"
        verbose_name_plural = "Особенности блюда"

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.strip().lower().capitalize()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Dish(django.db.models.Model):
    name = django.db.models.CharField(
        "название",
        max_length=100,
    )
    description = django.db.models.TextField(
        "описание состава",
        blank=True,
    )
    features = django.db.models.ManyToManyField(
        DishFeatures,
        blank=True,
        verbose_name="Особенности блюда",
        related_name="features",
    )

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"

    def __str__(self):
        return self.name.capitalize()


class Ingredient(django.db.models.Model):
    dish = django.db.models.ForeignKey(
        Dish,
        on_delete=django.db.models.CASCADE,
        related_name="ingredients",
    )
    name = django.db.models.CharField(
        "ингредиент",
        max_length=50,
    )
    quantity = django.db.models.IntegerField("количество")
    unit = django.db.models.CharField(
        "единица",
        max_length=10,
        choices=[
            ("г", "г"),
            ("мл", "мл"),
            ("шт", "шт"),
        ],
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def clean(self):
        if re.search(r"\d", self.name):
            raise django.core.exceptions.ValidationError(
                {"name": "Название ингредиента не должно содержать цифры"},
            )

        if self.quantity <= 0 or self.quantity > 100000:
            raise django.core.exceptions.ValidationError(
                {"quantity": "Количество должно быть больше 0"},
            )

    def __str__(self):
        return f"{self.name} — {self.quantity} {self.unit}"


class BreakfastMenu(django.db.models.Model):
    drink1 = django.db.models.ForeignKey(
        Dish,
        on_delete=django.db.models.PROTECT,
        null=True,
        blank=True,
        related_name="breakfast_drink1",
    )
    drink2 = django.db.models.ForeignKey(
        Dish,
        on_delete=django.db.models.PROTECT,
        null=True,
        blank=True,
        related_name="breakfast_drink2",
    )

    dish1 = django.db.models.ForeignKey(
        Dish,
        on_delete=django.db.models.PROTECT,
        null=True,
        blank=True,
        related_name="breakfast_dish1",
    )

    dish2 = django.db.models.ForeignKey(
        Dish,
        on_delete=django.db.models.PROTECT,
        null=True,
        blank=True,
        related_name="breakfast_dish2",
    )

    class Meta:
        verbose_name = "Завтрак"
        verbose_name_plural = "Завтраки"

    def __str__(self):
        return "Завтрак"


class LunchMenu(django.db.models.Model):
    drink1 = django.db.models.ForeignKey(
        Dish,
        on_delete=django.db.models.PROTECT,
        null=True,
        blank=True,
        related_name="lunch_drink1",
    )
    drink2 = django.db.models.ForeignKey(
        Dish,
        on_delete=django.db.models.PROTECT,
        null=True,
        blank=True,
        related_name="lunch_drink2",
    )

    soup1 = django.db.models.ForeignKey(
        Dish,
        on_delete=django.db.models.PROTECT,
        null=True,
        blank=True,
        related_name="lunch_soup1",
    )
    soup2 = django.db.models.ForeignKey(
        Dish,
        on_delete=django.db.models.PROTECT,
        null=True,
        blank=True,
        related_name="lunch_soup2",
    )

    main = django.db.models.ForeignKey(
        Dish,
        on_delete=django.db.models.PROTECT,
        null=True,
        blank=True,
        related_name="lunch_main",
    )

    salad1 = django.db.models.ForeignKey(
        Dish,
        on_delete=django.db.models.PROTECT,
        null=True,
        blank=True,
        related_name="lunch_salad1",
    )
    salad2 = django.db.models.ForeignKey(
        Dish,
        on_delete=django.db.models.PROTECT,
        null=True,
        blank=True,
        related_name="lunch_salad2",
    )

    class Meta:
        verbose_name = "Обед"
        verbose_name_plural = "Обеды"

    def __str__(self):
        return "Обед"
