import zoneinfo
from logging import getLogger

import pytz
from django.conf import settings
from django.utils import timezone, translation

from .utils import get_language_code

logger = getLogger(__file__)


class TimeZoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tz_header = request.headers.get("TZ")

        if tz_header:
            try:
                timezone.activate(tz_header)
            except (pytz.UnknownTimeZoneError, zoneinfo.ZoneInfoNotFoundError):
                logger.error("Invalid timezone %s", tz_header)
                pass  # Handle unknown timezone error here
        else:
            # Set default timezone if TZ header is not provided
            timezone.activate("UTC")

        response = self.get_response(request)
        timezone.deactivate()
        return response


class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract language from _lang query parameter
        lang = request.GET.get("_lang")

        # Store the current language
        cur_language = translation.get_language()
        if lang:
            lang = get_language_code(lang).upper()
        if lang and lang.upper() in [code[0].upper() for code in settings.LANGUAGES]:
            # Activate the new language if it's valid
            translation.activate(lang)
        else:
            # Fallback to default language if not valid
            translation.activate(settings.LANGUAGE_CODE)

        response = self.get_response(request)

        # Restore the original language
        translation.activate(cur_language)

        return response
