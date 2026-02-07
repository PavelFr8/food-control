import django.forms

import inventory.models


class ItemForm(django.forms.ModelForm):
    class Meta:
        model = inventory.models.Item
        fields = (
            "name",
            "unit",
            "quantity",
        )


class ProcurementRequestForm(django.forms.ModelForm):
    class Meta:
        model = inventory.models.ProcurementRequest
        fields = (
            "item_name",
            "unit",
            "quantity",
        )


class ProcurementReviewForm(django.forms.ModelForm):
    class Meta:
        model = inventory.models.ProcurementRequest
        fields = (
            "status",
            "comment",
        )
