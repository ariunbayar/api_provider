from collections import defaultdict
from datetime import datetime

from django.db import transaction, DatabaseError
from django.db import models
from django.conf import settings

from table.models import Table
from column.models import Column
from value.models import Value
from main.utils import NonDeletedManager
from error.utils import track_error


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


class TableNotFoundError(Exception):
    pass

class ColumnsExcessiveError(Exception):
    pass

class ColumnsMissingError(Exception):
    pass

class ColumnValueError(Exception):
    def __init__(self, message, column_name=None):
        super().__init__(message, column_name)
        self.column_name = column_name

class BooleanValueError(ColumnValueError):
    pass

class IntegerValueError(ColumnValueError):
    pass

class IntegerLimitError(ColumnValueError):
    pass

class Char250ValueError(ColumnValueError):
    pass

class DateTimeValueError(ColumnValueError):
    pass

class RecordSaveError(Exception):
    pass

class DatatypeUndefinedError(Exception):
    pass


class RecordModel():

    def __init__(self, table, columns, data):

        self.table = table
        self.columns = columns

        self.record = Record()
        self.record.table = table

        self.values = []
        for column in columns:
            value = Value()
            value.column = column
            value.record = self.record
            if column.datatype == 'bool':
                value.value_bool = data.get(column.name)
            if column.datatype == 'int':
                value.value_int = data.get(column.name)
            if column.datatype == 'char_250':
                value.value_char_250 = data.get(column.name)
            if column.datatype == 'text':
                value.value_text = data.get(column.name)
            if column.datatype == 'datetime':
                value.value_datetime = data.get(column.name)
            self.values.append(value)

    def save(self):
        with transaction.atomic():
            self.record.save()
            for value in self.values:
                value.record = self.record
            Value.objects.bulk_create(self.values)

    def jsonable(self):

        values = {
                'pk': self.record.pk,
            }

        for value in self.values:

            column = value.column

            if column.datatype == 'bool':
                values[column.name] = value.value_bool

            if column.datatype == 'int':
               values[column.name] = value.value_int

            if column.datatype == 'char_250':
               values[column.name] = value.value_char_250

            if column.datatype == 'text':
               values[column.name] = value.value_text

            if column.datatype == 'datetime':
               values[column.name] = value.value_datetime.strftime(settings.DATETIME_API_FORMAT)

        return values


class RecordModelFactory():

    def __init__(self, table_slug):

        try:
            table = Table.obs.get(slug=table_slug)
        except Table.DoesNotExist:
            raise TableNotFoundError

        self.table = table
        self.columns = Column.obs.filter(table=table).order_by('pk')

    def clean(self, values):

        column_names = set([column.name for column in self.columns])
        column_names_dirty = set(values.keys())

        # sanitize column names

        columns_excessive = column_names_dirty - column_names
        if columns_excessive:
            raise ColumnsExcessiveError

        columns_missing = column_names - column_names_dirty
        if columns_missing:
            raise ColumnsMissingError

        # sanitize column values

        cleaned_data = {}
        for column in self.columns:
            value = values.get(column.name)
            if column.datatype == 'bool':
                cleaned_data[column.name] = self.clean_bool(column, value)
            if column.datatype == 'int':
                cleaned_data[column.name] = self.clean_int(column, value)
            if column.datatype == 'char_250':
                cleaned_data[column.name] = self.clean_char_250(column, value)
            if column.datatype == 'text':
                cleaned_data[column.name] = self.clean_text(column, value)
            if column.datatype == 'datetime':
                cleaned_data[column.name] = self.clean_datetime(column, value)

        return cleaned_data

    def clean_bool(self, column, value):
        true_values = ['yes', '1', 'true', 'on']
        false_values = ['no', '0', 'false', 'off']

        is_true = value in true_values
        is_false = value in false_values

        if not is_true and not is_false:
            raise BooleanValueError('error', column.name)

        return is_true

    def clean_int(self, column, value):
        try:
            value = int(value)
        except ValueError:
            raise IntegerValueError('error', column.name)

        if -0x80000000 > value or 0x7fffffff < value:
            raise IntegerLimitError('error', column.name)

        return value

    def clean_char_250(self, column, value):
        if isinstance(value, str) and len(value) <= 250:
            return value

        raise Char250ValueError('error', column.name)

    def clean_text(self, column, value):
        return value

    def clean_datetime(self, column, value):
        try:
            # XXX Microseconds included to: https://en.wikipedia.org/wiki/ISO_8601
            value = datetime.strptime(value, settings.DATETIME_API_FORMAT)
        except ValueError:
            raise DateTimeValueError('error', column.name)

        return value

    def create(self, values):

        cleaned_data = self.clean(values)

        try:
            obj = RecordModel(self.table, self.columns, cleaned_data)
            obj.save()
        except Exception as e:
            raise RecordSaveError

        return obj

    def value_to_jsonable(self, datatype, **datatype_values):

            if datatype == 'bool':
                return datatype_values['value_bool']

            if datatype == 'int':
                return datatype_values['value_int']

            if datatype == 'char_250':
                return datatype_values['value_char_250']

            if datatype == 'text':
                return datatype_values['value_text']

            if datatype == 'datetime':
                return datatype_values['value_datetime'].strftime(settings.DATETIME_API_FORMAT)

            raise DatatypeUndefinedError

    def fetch(self):

        fields_ref = ['record_id', 'column_id']
        fields_value = ['value_bool', 'value_int', 'value_char_250', 'value_text', 'value_datetime']

        qs = Value.objects.filter(record__table=self.table).order_by('record', 'column')
        values = qs.values_list(*fields_ref, *fields_value)

        column_pk_to_column = dict((col.pk, col) for col in self.columns)

        # TODO use generators for performance
        obj_ref = defaultdict(dict)

        for record_id, column_id, *value_list in values:

            column = column_pk_to_column[column_id]
            value = self.value_to_jsonable(column.datatype, **dict(zip(fields_value, value_list)))

            obj_ref[record_id][column.name] = value

        obj_list = []
        for pk, obj in obj_ref.items():
            obj_list.append({'pk': pk, **obj})

        return obj_list
