from .models import Error, ErrorType


def track_error(tracking_number, error_code):

    try:
        error_type = ErrorType.objects.get(code=error_code)
    except ErrorType.DoesNotExist:
        # TODO notify to admin only
        raise Exception('ERROR: ErrorType of code "%s" is not found' % error_code)

    error = Error.objects.create(request_id=tracking_number, error_type=error_type)

    return error
