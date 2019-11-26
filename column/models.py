from django.db import models

from table.models import Table
from main.utils import NonDeletedManager


class Column(models.Model):

    obs = NonDeletedManager()

    DATATYPES = [
            ('bool', 'Boolean'),
            ('int', 'Integer'),
            ('char_250', 'Char(250)'),
            ('text', 'Text'),
            ('datetime', 'Datetime'),
        ]

    table = models.ForeignKey(Table, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    datatype = models.CharField(max_length=50, choices=DATATYPES, db_index=True)

    is_deleted = models.BooleanField(default=False, db_index=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
