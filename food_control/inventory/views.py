import django.contrib.auth.mixins
import django.shortcuts
import django.urls
import django.utils.timezone
import django.views.generic

import inventory.forms
import inventory.models
import notifications.services
import users.forms
import users.models


class StockListView(
    users.forms.RoleRequiredMixin,
    django.views.generic.ListView,
):
    required_roles = [
        users.models.Role.RoleNames.COOK,
        users.models.Role.RoleNames.ADMIN,
    ]
    model = inventory.models.StockItem
    template_name = "inventory/stock_list.html"
    context_object_name = "stock_items"


class StockCreateView(
    users.forms.RoleRequiredMixin,
    django.views.generic.CreateView,
):
    required_roles = [
        users.models.Role.RoleNames.COOK,
        users.models.Role.RoleNames.ADMIN,
    ]
    model = inventory.models.StockItem
    form_class = inventory.forms.StockItemForm
    template_name = "inventory/stock_form.html"

    def get_success_url(self):
        return django.urls.reverse("inventory:stock_list")


class StockUpdateView(
    users.forms.RoleRequiredMixin,
    django.views.generic.UpdateView,
):
    required_roles = [
        users.models.Role.RoleNames.COOK,
        users.models.Role.RoleNames.ADMIN,
    ]
    model = inventory.models.StockItem
    form_class = inventory.forms.StockItemForm
    template_name = "inventory/stock_form.html"

    def get_success_url(self):
        return django.urls.reverse("inventory:stock_list")


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
            qs = qs.filter(created_by=self.request.user)
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
        response = super().form_valid(form)

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
        return response

    def get_success_url(self):
        return django.urls.reverse("inventory:procurement_list")

    def get_queryset(self):
        return super().get_queryset().select_related("created_by")
