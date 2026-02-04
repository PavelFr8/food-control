import django.urls
import django.views.generic.edit

import rating.models
import users.forms


class DeleteRatingView(
    django.views.generic.edit.DeleteView,
    users.forms.RoleRequiredMixin,
):
    model = rating.models.Rating

    def get_success_url(self):
        return django.urls.reverse_lazy(
            "menu:dish_detail",
            kwargs={"pk": self.object.dish.pk},
        )

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
