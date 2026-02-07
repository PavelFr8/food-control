import django.contrib.auth.mixins
import django.shortcuts
import django.urls
import django.views.generic

import notifications.models


class NotificationListView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.ListView,
):
    model = notifications.models.Notification
    template_name = "notifications/notifications.html"
    context_object_name = "notifications"
    paginate_by = 20

    def get_queryset(self):
        return notifications.models.Notification.objects.filter(
            user=self.request.user,
        )


class MarkAllReadView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.View,
):
    def post(self, request, *args, **kwargs):
        notifications.models.Notification.objects.filter(
            user=request.user,
            is_read=False,
        ).update(is_read=True)
        return django.shortcuts.redirect(
            django.urls.reverse("notifications:list"),
        )
