import django.urls

import inventory.views

app_name = "inventory"

urlpatterns = [
    django.urls.path(
        "stock/",
        inventory.views.StockListView.as_view(),
        name="stock_list",
    ),
    django.urls.path(
        "stock/add/",
        inventory.views.StockCreateView.as_view(),
        name="stock_add",
    ),
    django.urls.path(
        "stock/<int:pk>/edit/",
        inventory.views.StockUpdateView.as_view(),
        name="stock_edit",
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
