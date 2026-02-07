import django.contrib.admin

import notifications.models


@django.contrib.admin.register(notifications.models.Notification)
class NotificationAdmin(django.contrib.admin.ModelAdmin):
    list_display = ("title", "user", "is_read", "created_at")
    list_filter = ("is_read",)
    search_fields = ("title", "message", "user__email")
