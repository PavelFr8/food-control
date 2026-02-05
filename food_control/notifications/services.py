import notifications.models


def notify_user(*, user, title, message, link=""):
    notifications.models.Notification.objects.create(
        user=user,
        title=title,
        message=message,
        link=link,
    )
