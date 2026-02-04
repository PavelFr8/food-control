import django.contrib.auth.mixins
import django.urls
import django.views.generic

import payments.forms
import payments.services
import users.forms


class PaymentCreateView(
    django.views.generic.FormView,
    users.forms.RoleRequiredMixin,
):
    template_name = "payments/payment.html"
    form_class = payments.forms.PaymentForm
    success_url = django.urls.reverse_lazy("users:profile")

    def form_valid(self, form):
        payments.services.apply_payment(
            user=self.request.user,
            payment_type=form.cleaned_data["payment_type"],
            idempotency_key=form.cleaned_data["idempotency_key"],
        )
        return super().form_valid(form)
