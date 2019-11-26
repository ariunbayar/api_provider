from django.conf import settings

from notification.models import Notification


def context_processor(request):
    notifications = Notification.objects.filter(is_read=False)

    return {
        'notifications': notifications,
    }
