from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import (
        RecordModelFactory,
        TableNotFoundError,
        ColumnsExcessiveError,
        ColumnsMissingError,
        BooleanValueError,
        IntegerValueError,
        IntegerLimitError,
        Char250ValueError,
        DateTimeValueError,
        RecordSaveError,
        DatatypeUndefinedError,
    )
from error.utils import track_error


# TODO api_authentication
@require_POST
@csrf_exempt
def insert(request, table_slug):

    def track_error_and_rsp(error_code, message):
        track_error(request.tracking_number, error_code)
        return JsonResponse({'success': False, 'error': message})

    factory = RecordModelFactory(table_slug)

    try:

        obj = factory.create(request.POST)

    except TableNotFoundError:

        return track_error_and_rsp('E404-1', 'Table not found')

    except ColumnsExcessiveError:

        column_names = ','.join(['"%s"' % c.name for c in factory.columns])
        return track_error_and_rsp('E501-1', 'Excessive fields. Requires: ' + column_names)

    except ColumnsMissingError:

        column_names = ','.join(['"%s"' % c.name for c in factory.columns])
        return track_error_and_rsp('E501-2', 'Missing fields. Requires: ' + column_names)

    except BooleanValueError as e:

        return track_error_and_rsp('E101-1', 'Invalid boolean value for "%s".' % e.column_name)

    except IntegerValueError as e:

        return track_error_and_rsp('E101-2', 'Invalid integer value for "%s".' % e.column_name)

    except IntegerLimitError as e:

        return track_error_and_rsp('E001-1', 'Integer for "%s" must be between -2147483648 to 2147483647.' % e.column_name)

    except Char250ValueError as e:

        return track_error_and_rsp('E101-3', 'Maximum length for "%s" must be 250.' % e.column_name)

    except DateTimeValueError as e:

        return track_error_and_rsp('E101-4', 'Format for "%s" must be "YYYY-MM-DDThh:mm:ss.sss±hhmm".' % e.column_name)

    except RecordSaveError as e:

        return track_error_and_rsp('E501-3', 'Cannot store object')

    rsp = {
            'success': True,
            obj.table.name: obj.jsonable(),
        }

    return JsonResponse(rsp)


@require_GET
def fetch(request, table_slug):

    def track_error_and_rsp(error_code, message):
        track_error(request.tracking_number, error_code)
        return JsonResponse({'success': False, 'error': message})


    factory = RecordModelFactory(table_slug)

    try:

        obj_list = factory.fetch()

    except TableNotFoundError:

        return track_error_and_rsp('E404-2', 'Table not found')

    except DatatypeUndefinedError:

        return track_error_and_rsp('E900-1', 'API error')

    rsp = {
            'success': True,
            factory.table.name: obj_list,
        }

    return JsonResponse(rsp)
