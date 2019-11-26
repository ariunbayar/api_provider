from django.db import models
from django.conf import settings


class Request(models.Model):

    class Meta:
        ordering = ('-started_at',)

    METHOD_CHOICES = [('POST', 'Post'), ('GET', 'Get')]

    is_ajax = models.BooleanField()
    url = models.CharField(max_length=500)
    url_name = models.CharField(max_length=50, null=True)
    user_agent = models.CharField(max_length=500)
    referer = models.CharField(max_length=500, null=True)
    redirect_url = models.CharField(max_length=500, null=True)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    ip_addr = models.GenericIPAddressField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
    started_at = models.DateTimeField()
    duration_ms = models.IntegerField(null=True)
    request_size = models.IntegerField()
    response_size = models.IntegerField(null=True)
    status_code = models.IntegerField(null=True)
