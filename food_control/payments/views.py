from datetime import timedelta

import django.db.models
import django.http
import django.urls
import django.utils.dateparse
import django.utils.timezone
import django.views.generic

import meals.models
import payments.forms
import payments.models
import payments.services
import users.forms
import users.models


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


class AdminStatsView(
    users.forms.RoleRequiredMixin,
    django.views.generic.TemplateView,
):
    required_roles = [users.models.Role.RoleNames.ADMIN]
    template_name = "payments/admin_stats.html"

    def _get_date_range(self):
        today = django.utils.timezone.now().date()

        start_param = self.request.GET.get("start")
        end_param = self.request.GET.get("end")

        start_date = (
            django.utils.dateparse.parse_date(start_param)
            if isinstance(start_param, str)
            else None
        )
        end_date = (
            django.utils.dateparse.parse_date(end_param)
            if isinstance(end_param, str)
            else None
        ) or today

        if not start_date:
            start_date = end_date - timedelta(days=6)

        if start_date > end_date:
            start_date, end_date = end_date, start_date

        return start_date, end_date

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_date, end_date = self._get_date_range()

        payments_qs = payments.models.Payment.objects.filter(
            created__date__range=(start_date, end_date),
            is_success=True,
        )
        meals_qs = meals.models.Meal.objects.filter(
            date__range=(start_date, end_date),
        )

        payment_stats = payments_qs.aggregate(
            total_amount=django.db.models.Sum("amount"),
            total_count=django.db.models.Count("id"),
        )

        attendance_count = meals_qs.count()

        payment_by_day = (
            payments_qs.values("created__date")
            .annotate(
                total=django.db.models.Sum("amount"),
                count=django.db.models.Count("id"),
            )
            .order_by("created__date")
        )
        meals_by_day = (
            meals_qs.values("date")
            .annotate(count=django.db.models.Count("id"))
            .order_by("date")
        )

        context.update(
            {
                "start_date": start_date,
                "end_date": end_date,
                "total_amount": payment_stats["total_amount"] or 0,
                "total_count": payment_stats["total_count"],
                "attendance_count": attendance_count,
                "payment_by_day": payment_by_day,
                "meals_by_day": meals_by_day,
            },
        )
        return context


class AdminReportDownloadView(
    users.forms.RoleRequiredMixin,
    django.views.generic.View,
):
    required_roles = [users.models.Role.RoleNames.ADMIN]

    def _get_date_range(self):
        today = django.utils.timezone.now().date()

        start_param = self.request.GET.get("start")
        end_param = self.request.GET.get("end")

        start_date = (
            django.utils.dateparse.parse_date(start_param)
            if isinstance(start_param, str)
            else None
        )
        end_date = (
            django.utils.dateparse.parse_date(end_param)
            if isinstance(end_param, str)
            else None
        ) or today

        if not start_date:
            start_date = end_date - timedelta(days=6)

        if start_date > end_date:
            start_date, end_date = end_date, start_date

        return start_date, end_date

    def get(self, request, *args, **kwargs):
        start_date, end_date = self._get_date_range()

        payments_qs = payments.models.Payment.objects.filter(
            created__date__range=(start_date, end_date),
            is_success=True,
        )
        meals_qs = meals.models.Meal.objects.filter(
            date__range=(start_date, end_date),
        )

        response = django.http.HttpResponse(
            content_type="text/csv",
        )
        response["Content-Disposition"] = (
            f"attachment; filename=report_{start_date}_{end_date}.csv"
        )

        response.write("Раздел,Дата,Количество,Сумма\\n")
        for row in (
            payments_qs.values("created__date")
            .annotate(
                total=django.db.models.Sum("amount"),
                count=django.db.models.Count("id"),
            )
            .order_by("created__date")
        ):
            response.write(
                f"Платежи,{row['created__date']},{row['count']},"
                f"{row['total']}\\n",
            )

        for row in (
            meals_qs.values("date")
            .annotate(count=django.db.models.Count("id"))
            .order_by("date")
        ):
            response.write(
                f"Посещаемость,{row['date']},{row['count']},\\n",
            )

        return response
