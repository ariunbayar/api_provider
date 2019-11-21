import threading

from django.utils.timezone import localtime, now

from request.models import Request
from main.utils import get_client_ip


class RequestLogMiddleware:
    """
    Credits to: https://github.com/Alir3z4/django-crequest/blob/master/crequest/middleware.py
    """

    _requests = {}

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        req = Request()
        req.referer = request.META.get('HTTP_REFERER')
        req.method = request.method
        req.user_agent = request.META.get('HTTP_USER_AGENT')
        req.ip_addr = get_client_ip(request)
        req.url = request.build_absolute_uri()
        req.request_size = len(request.body)
        req.is_ajax = request.is_ajax()

        if hasattr(request, 'user') and request.user.is_authenticated:
            req.user = request.user

        req.started_at = localtime(now())
        req.save()

        request.tracking_number = req.id

        self.__class__.set_request(request)
        response = self.get_response(request)
        self.__class__.del_request()

        if request.resolver_match:
            req.url_name = request.resolver_match.url_name
        req.response_size = len(response.content)
        req.redirect_url = response.get('Location')
        req.status_code = response.status_code
        req.duration_ms = (localtime(now()) - req.started_at).total_seconds() * 1000
        req.save()

        return response

    @classmethod
    def get_request(cls, default=None):
        """
        Retrieve the request object for the current thread, or the optionally
        provided default if there is no current request.
        """
        return cls._requests.get(threading.current_thread(), default)

    @classmethod
    def set_request(cls, request):
        """
        Save the given request into storage for the current thread.
        """
        cls._requests[threading.current_thread()] = request

    @classmethod
    def del_request(cls):
        """
        Delete the request that was stored for the current thread.
        """
        cls._requests.pop(threading.current_thread(), None)
