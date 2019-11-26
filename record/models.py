from django.db import models

from table.models import Table
from main.utils import NonDeletedManager


class Record(models.Model):
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

    obs = NonDeletedManager()

    table = models.ForeignKey(Table, on_delete=models.PROTECT)
    is_deleted = models.BooleanField(default=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
