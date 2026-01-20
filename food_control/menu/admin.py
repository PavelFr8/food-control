import django.contrib.admin

import menu.models
import rating.models


class DishInline(django.contrib.admin.TabularInline):
    model = menu.models.Ingredient
    extra = 0
    readonly_fields = ("name", "quantity", "unit")
    can_delete = False


class RatingInline(django.contrib.admin.TabularInline):
    model = rating.models.Rating
    extra = 0
    readonly_fields = (
        rating.models.Rating.mark.field.name,
        rating.models.Rating.user.field.name,
    )
    can_delete = False
    can_add = False


@django.contrib.admin.register(menu.models.Dish)
class DishAdmin(django.contrib.admin.ModelAdmin):
    list_display = ("name", "get_features")
    search_fields = ("name",)
    inlines = [DishInline]

    inlines = [RatingInline]

    def get_features(self, obj):
        return ", ".join([f.name for f in obj.features.all()])

    get_features.short_description = "Особенности"


@django.contrib.admin.register(menu.models.BreakfastMenu)
class BreakfastMenuAdmin(django.contrib.admin.ModelAdmin):
    list_display = ("__str__", "drink1", "drink2", "dish1", "dish2")
    list_select_related = ("drink1", "drink2", "dish1", "dish2")
    search_fields = (
        "drink1__name",
        "drink2__name",
        "dish1__name",
        "dish2__name",
    )


@django.contrib.admin.register(menu.models.LunchMenu)
class LunchMenuAdmin(django.contrib.admin.ModelAdmin):
    list_display = ("__str__", "drink1", "drink2", "soup1", "soup2", "main")
    list_select_related = ("drink1", "drink2", "soup1", "soup2", "main")
    search_fields = (
        "drink1__name",
        "drink2__name",
        "soup1__name",
        "soup2__name",
        "main__name",
    )
