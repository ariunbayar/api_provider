from django.db import models
from django.conf import settings

from main.utils import NonDeletedManager


class Table(models.Model):

    obs = NonDeletedManager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)

    is_deleted = models.BooleanField(default=False, db_index=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
