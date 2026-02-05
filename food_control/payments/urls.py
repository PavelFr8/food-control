import django.urls

import payments.views

app_name = "payments"

urlpatterns = [
    django.urls.path(
        "payment/",
        payments.views.PaymentCreateView.as_view(),
        name="payment",
    ),
    django.urls.path(
        "stats/",
        payments.views.AdminStatsView.as_view(),
        name="stats",
    ),
    django.urls.path(
        "stats/report/",
        payments.views.AdminReportDownloadView.as_view(),
        name="stats_report",
    ),
]
