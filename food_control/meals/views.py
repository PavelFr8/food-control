import django.contrib.auth.mixins
import django.shortcuts
import django.views.generic

import payments.services
import users.forms
import users.models


class ConsumeMealView(
    users.forms.RoleRequiredMixin,
    django.views.generic.View,
):
    required_roles = [
        users.models.Role.RoleNames.COOK,
    ]

    def post(self, request, *args, **kwargs):
        target_user = users.models.User.objects.get(pk=kwargs.get("user_id"))
        payments.services.consume_meal(
            user=target_user,
            meal_type=kwargs.get("meal_type"),
        )
        return django.shortcuts.redirect("meals:meals")


class StudentConsumeMealView(
    users.forms.RoleRequiredMixin,
    django.views.generic.View,
):
    required_roles = [
        users.models.Role.RoleNames.STUDENT,
    ]

    def post(self, request, *args, **kwargs):
        payments.services.consume_meal(
            user=request.user,
            meal_type=kwargs.get("meal_type"),
        )
        return django.shortcuts.redirect("users:profile")


class MealsView(users.forms.RoleRequiredMixin, django.views.generic.ListView):
    required_roles = [
        users.models.Role.RoleNames.ADMIN,
        users.models.Role.RoleNames.COOK,
    ]
    template_name = "meals/meals.html"
    context_object_name = "users"
    paginate_by = 20

    def get_queryset(self):
        qs = users.models.User.objects.get_students()

        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                django.db.models.Q(first_name__icontains=query)
                | django.db.models.Q(last_name__icontains=query),
            )

        return qs.order_by("first_name", "last_name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context
