import django.contrib.admin

import users.models


@django.contrib.admin.register(users.models.User)
class UserAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        users.models.User.email.field.name,
        users.models.User.first_name.field.name,
        users.models.User.last_name.field.name,
        users.models.User.role.field.name,
        users.models.User.is_active.field.name,
        users.models.User.date_joined.field.name,
    )

    list_filter = (
        users.models.User.role.field.name,
        users.models.User.is_active.field.name,
        users.models.User.date_joined.field.name,
    )
    filter_horizontal = (users.models.User.food_features.field.name,)

    search_fields = (
        users.models.User.email.field.name,
        users.models.User.first_name.field.name,
        users.models.User.last_name.field.name,
    )

    ordering = (f"-{users.models.User.date_joined.field.name}",)

    readonly_fields = (
        users.models.User.birthday.field.name,
        users.models.User.attempts_count.field.name,
        users.models.User.block_date.field.name,
        users.models.User.last_login.field.name,
        users.models.User.date_joined.field.name,
    )


@django.contrib.admin.register(users.models.FoodFeatures)
class FoodFeaturesAdmin(django.contrib.admin.ModelAdmin):
    list_display = (users.models.FoodFeatures.name.field.name,)
