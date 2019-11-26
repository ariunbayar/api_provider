from django.db import models
from django.conf import settings


class Notification(models.Model):

    class Meta:
        ordering = ['-created_at']

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
