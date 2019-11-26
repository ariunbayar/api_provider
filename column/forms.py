from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm

from .models import Column


class ColumnForm(ModelForm):

    class Meta:

        model = Column

        fields = ['table', 'name', 'datatype']

        widgets = {
                'table': forms.HiddenInput(),
            }

        labels = {
                'name': 'Нэр:',
                'datatype': 'Төрөл:',
            }

        error_messages = {
                'name': {
                        'required': 'Оруулна уу!',
                        'invalid': 'Зөв оруулна уу!',
                        'max_length': '%(limit_value)d илүүгүй урттай оруулна уу!',
                    },
                'datatype': {
                        'required': 'Сонгоно уу!',
                        'invalid_choice': 'Сонгоно уу!',
                    },
                NON_FIELD_ERRORS: {},
            }

        help_texts = {}
