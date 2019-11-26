from .models import Notification


def notify(user, message):
    notification = Notification.objects.create(
            user=user,
            message=message,
        )
    return notification
