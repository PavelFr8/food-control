import django.apps


class InventoryConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "inventory"
    verbose_name = "Склад и закупки"
