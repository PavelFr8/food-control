import django.urls

import payments.views

app_name = "payments"

urlpatterns = [
    django.urls.path(
        "payment/",
        payments.views.PaymentCreateView.as_view(),
        name="payment",
    ),
]
