from django.db import models

from column.models import Column


class Value(models.Model):
    """
    +----------+      +----------+
    |  Table   | <--- |  Column  |
    +----------+      +----------+
          ^                 ^
          |                 |
    +----------+      +----------+
    |  Record  | <--- |  Value   |
    +----------+      +----------+
    """

    column = models.ForeignKey(Column, on_delete=models.PROTECT)
    record = models.ForeignKey('record.Record', on_delete=models.PROTECT)

    value_bool = models.BooleanField(null=True, db_index=True)
    value_int = models.IntegerField(null=True, db_index=True)
    value_char_250 = models.CharField(max_length=250, null=True, db_index=True)
    value_text = models.TextField(null=True)
    value_datetime = models.DateTimeField(null=True, db_index=True)
