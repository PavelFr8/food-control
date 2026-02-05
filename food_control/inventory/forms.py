import django.forms

import inventory.models


class StockItemForm(django.forms.ModelForm):
    class Meta:
        model = inventory.models.StockItem
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
