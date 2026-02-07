import django.urls

import inventory.views

app_name = "inventory"

urlpatterns = [
    django.urls.path(
        "item/",
        inventory.views.ItemListView.as_view(),
        name="item_list",
    ),
    django.urls.path(
        "item/add/",
        inventory.views.ItemCreateView.as_view(),
        name="item_add",
    ),
    django.urls.path(
        "item/<int:pk>/edit/",
        inventory.views.ItemUpdateView.as_view(),
        name="item_edit",
    ),
    django.urls.path(
        "procurements/",
        inventory.views.ProcurementRequestListView.as_view(),
        name="procurement_list",
    ),
    django.urls.path(
        "procurements/add/",
        inventory.views.ProcurementRequestCreateView.as_view(),
        name="procurement_add",
    ),
    django.urls.path(
        "procurements/<int:pk>/review/",
        inventory.views.ProcurementRequestReviewView.as_view(),
        name="procurement_review",
    ),
]
