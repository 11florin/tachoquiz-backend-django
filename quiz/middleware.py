from zoneinfo import ZoneInfo

from django.utils import timezone


class TimezoneMiddleware:
    """Activate the timezone stored in the user's session."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        timezone_name = request.session.get("user_timezone")

        if timezone_name:
            timezone.activate(ZoneInfo(timezone_name))
        else:
            timezone.deactivate()

        response = self.get_response(request)

        return response