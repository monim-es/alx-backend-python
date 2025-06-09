# chats/middleware.py
import logging
from datetime import datetime, time as dt_time
import time as time_module
from django.http import HttpResponseForbidden, JsonResponse
from collections import defaultdict

# Configure global logger
logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logger  # Use configured logger

    def __call__(self, request):
        response = self.get_response(request)
        user = request.user if request.user.is_authenticated else "Anonymous"
        self.logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        start = dt_time(18, 0)  # 6:00 PM
        end = dt_time(21, 0)    # 9:00 PM

        if not (start <= now <= end):
            return HttpResponseForbidden("Chat access is allowed only between 6PM and 9PM.")

        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = defaultdict(list)
        self.message_limit = 5
        self.time_window = 60  # seconds

    def __call__(self, request):
        if request.method == 'POST' and request.path.endswith('/messages/'):
            ip = self.get_client_ip(request)
            now = time_module.time()

            # Clean old timestamps
            self.message_log[ip] = [ts for ts in self.message_log[ip] if now - ts < self.time_window]

            if len(self.message_log[ip]) >= self.message_limit:
                return JsonResponse(
                    {'error': 'Message limit exceeded. Try again later.'},
                    status=429
                )

            self.message_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only enforce on authenticated users
        if request.user.is_authenticated:
            # Only allow users with is_staff (admin/moderator) to access sensitive endpoints
            if not request.user.is_staff and request.path.startswith('/api/chats/'):
                return HttpResponseForbidden("Only admins or moderators are allowed to perform this action.")
        return self.get_response(request)