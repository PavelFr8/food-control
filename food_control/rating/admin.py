import django.contrib.admin

import rating.models


@django.contrib.admin.register(rating.models.Rating)
class RatingAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        rating.models.Rating.dish.field.name,
        rating.models.Rating.user.field.name,
        rating.models.Rating.mark.field.name,
    )
    list_filter = (rating.models.Rating.mark.field.name,)
    ordering = (rating.models.Rating.mark.field.name,)
    readonly_fields = (
        rating.models.Rating.dish.field.name,
        rating.models.Rating.user.field.name,
        rating.models.Rating.mark.field.name,
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
