import django.urls
import django.utils.timezone
import django.views.generic

import inventory.forms
import inventory.models
import notifications.services
import users.forms
import users.models


class ItemListView(
    users.forms.RoleRequiredMixin,
    django.views.generic.ListView,
):
    required_roles = [
        users.models.Role.RoleNames.COOK,
        users.models.Role.RoleNames.ADMIN,
    ]
    model = inventory.models.Item
    template_name = "inventory/item_list.html"
    context_object_name = "items"


class ItemCreateView(
    users.forms.RoleRequiredMixin,
    django.views.generic.CreateView,
):
    required_roles = [
        users.models.Role.RoleNames.COOK,
        users.models.Role.RoleNames.ADMIN,
    ]
    model = inventory.models.Item
    form_class = inventory.forms.ItemForm
    template_name = "inventory/item_form.html"

    def get_success_url(self):
        return django.urls.reverse("inventory:item_list")


class ItemUpdateView(
    users.forms.RoleRequiredMixin,
    django.views.generic.UpdateView,
):
    required_roles = [
        users.models.Role.RoleNames.COOK,
        users.models.Role.RoleNames.ADMIN,
    ]
    model = inventory.models.Item
    form_class = inventory.forms.ItemForm
    template_name = "inventory/item_form.html"

    def get_success_url(self):
        return django.urls.reverse("inventory:item_list")


class ProcurementRequestListView(
    users.forms.RoleRequiredMixin,
    django.views.generic.ListView,
):
    required_roles = [
        users.models.Role.RoleNames.COOK,
        users.models.Role.RoleNames.ADMIN,
    ]
    model = inventory.models.ProcurementRequest
    template_name = "inventory/procurement_list.html"
    context_object_name = "requests"

    def get_queryset(self):
        qs = super().get_queryset().select_related("created_by", "reviewed_by")
        if self.request.user.role.name == users.models.Role.RoleNames.COOK:
            return qs.filter(created_by=self.request.user)

        return qs


class ProcurementRequestCreateView(
    users.forms.RoleRequiredMixin,
    django.views.generic.CreateView,
):
    required_roles = [
        users.models.Role.RoleNames.COOK,
    ]
    model = inventory.models.ProcurementRequest
    form_class = inventory.forms.ProcurementRequestForm
    template_name = "inventory/procurement_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return django.urls.reverse("inventory:procurement_list")


class ProcurementRequestReviewView(
    users.forms.RoleRequiredMixin,
    django.views.generic.UpdateView,
):
    required_roles = [
        users.models.Role.RoleNames.ADMIN,
    ]
    model = inventory.models.ProcurementRequest
    form_class = inventory.forms.ProcurementReviewForm
    template_name = "inventory/procurement_review.html"

    def form_valid(self, form):
        form.instance.reviewed_by = self.request.user
        form.instance.reviewed_at = django.utils.timezone.now()

        notifications.services.notify_user(
            user=form.instance.created_by,
            title="Статус заявки на закупку",
            message=(
                f"Заявка на {form.instance.item_name} "
                f"({form.instance.quantity} {form.instance.unit}) — "
                f"{form.instance.get_status_display().lower()}."
            ),
            link=django.urls.reverse("inventory:procurement_list"),
        )
        return super().form_valid(form)

    def get_success_url(self):
        return django.urls.reverse("inventory:procurement_list")

    def get_queryset(self):
        return super().get_queryset().select_related("created_by")
