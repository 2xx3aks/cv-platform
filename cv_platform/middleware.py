"""
Custom middleware to debug and ensure language is applied correctly.
"""
from django.utils import translation
from django.conf import settings


class LanguageDebugMiddleware:
    """
    Debug middleware to ensure language is applied correctly.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check language sources
        lang_from_session = request.session.get('django_language')
        lang_from_cookie = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
        
        # Determine language (cookie takes precedence, then session, then default)
        if lang_from_cookie and lang_from_cookie in [lang[0] for lang in settings.LANGUAGES]:
            language = lang_from_cookie
        elif lang_from_session and lang_from_session in [lang[0] for lang in settings.LANGUAGES]:
            language = lang_from_session
        else:
            language = settings.LANGUAGE_CODE
        
        # Activate language
        translation.activate(language)
        request.LANGUAGE_CODE = language
        
        response = self.get_response(request)
        
        return response

