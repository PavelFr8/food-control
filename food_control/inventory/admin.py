import django.contrib.admin

import inventory.models


@django.contrib.admin.register(inventory.models.StockItem)
class StockItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = ("name", "quantity", "unit", "updated_at")
    search_fields = ("name",)


@django.contrib.admin.register(inventory.models.ProcurementRequest)
class ProcurementRequestAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        "item_name",
        "quantity",
        "unit",
        "status",
        "created_by",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = ("item_name", "created_by__email")
