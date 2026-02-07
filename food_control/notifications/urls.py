import django.urls

import notifications.views

app_name = "notifications"

urlpatterns = [
    django.urls.path(
        "",
        notifications.views.NotificationListView.as_view(),
        name="list",
    ),
    django.urls.path(
        "mark-all/",
        notifications.views.MarkAllReadView.as_view(),
        name="mark_all",
    ),
]
