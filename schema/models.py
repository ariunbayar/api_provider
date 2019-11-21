from django.db import models

from request.models import Request


class Rev(models.Model):

    class Meta:
        ordering = ('-created_at',)

    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]

    request = models.ForeignKey(Request, on_delete=models.PROTECT)
    model = models.CharField(max_length=50, db_index=True)
    object_id  = models.IntegerField(db_index=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)


class RevField(models.Model):

    FIELD_TYPES = [
            ('bool', 'Boolean'),
            ('int', 'Integer'),
            ('text', 'Text'),
            ('blob', 'Blob'),
            ('datetime', 'Datetime'),
        ]

    model = models.CharField(max_length=50, db_index=True)
    field_name = models.CharField(max_length=50, db_index=True)
    field_type = models.CharField(max_length=50, choices=FIELD_TYPES, db_index=True)
    foreign_key = models.ForeignKey('self', on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class RevValue(models.Model):

    rev = models.ForeignKey(Rev, on_delete=models.PROTECT)
    field = models.ForeignKey(RevField, on_delete=models.PROTECT)
    value      = models.CharField(max_length=4000, null=True, blank=True)
    value_bin  = models.BinaryField(null=True)
