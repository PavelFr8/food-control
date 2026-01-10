import django.contrib.admin

import users.models


User = users.models.User


@django.contrib.admin.register(User)
class UserAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        User.email.field.name,
        User.first_name.field.name,
        User.last_name.field.name,
        User.role.field.name,
        User.is_active.field.name,
        User.date_joined.field.name,
    )

    list_filter = (
        User.role.field.name,
        User.is_active.field.name,
        User.date_joined.field.name,
    )

    search_fields = (
        User.email.field.name,
        User.first_name.field.name,
        User.last_name.field.name,
    )

    ordering = (f"-{User.date_joined.field.name}",)

    readonly_fields = (
        User.birthday.field.name,
        User.attempts_count.field.name,
        User.block_date.field.name,
        User.last_login.field.name,
        User.date_joined.field.name,
    )
