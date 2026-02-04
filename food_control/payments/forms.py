import uuid

import django.forms

import payments.models


class PaymentForm(django.forms.Form):
    payment_type = django.forms.ChoiceField(
        choices=payments.models.Payment.PaymentType.choices,
        widget=django.forms.RadioSelect,
        label="Тип оплаты",
    )

    idempotency_key = django.forms.UUIDField(
        widget=django.forms.HiddenInput,
        initial=uuid.uuid4,
    )
