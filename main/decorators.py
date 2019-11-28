from django.shortcuts import redirect
from django.http import HttpResponseServerError

from error.utils import track_error

from . import exceptions


def track_exceptions(f):

    def wrap(request, *args, **kwargs):
        try:
            return f(request, *args, **kwargs)
        except exceptions.AppError as e:
            track_error(request.tracking_number, str(e))
            raise e

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
