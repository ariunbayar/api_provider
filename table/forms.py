from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm

from .models import Table


class TableForm(ModelForm):

    class Meta:

        model = Table

        fields = ['name']

        widgets = {}

        labels = {
                'name': 'Нэр:',
            }

        error_messages = {
                'name': {
                        'required': 'Оруулна уу!',
                        'invalid': 'Зөв оруулна уу!',
                        'max_length': '%(limit_value)d илүүгүй урттай оруулна уу!',
                    },
                NON_FIELD_ERRORS: {},
            }

        help_texts = {}
