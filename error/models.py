from django.db import models

from request.models import Request


class ErrorType(models.Model):
    code = models.CharField(max_length=10, unique=True, db_index=True)
    summary = models.CharField(max_length=250)
    description = models.TextField(null=True)


class Error(models.Model):
    error_type = models.ForeignKey(ErrorType, on_delete=models.PROTECT)
    request = models.ForeignKey(Request, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
