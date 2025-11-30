"""
Custom context processors for templates.
"""
from django.utils import translation
from django.conf import settings


def language_processor(request):
    """Add current language and LANGUAGES to template context."""
    # Get current language from request
    current_lang = translation.get_language()
    
    # If no language is set, use default
    if not current_lang or current_lang not in [lang[0] for lang in settings.LANGUAGES]:
        current_lang = settings.LANGUAGE_CODE
    
    return {
        'current_language': current_lang,
        'LANGUAGE_CODE': current_lang,
        'LANGUAGES': settings.LANGUAGES,  # Make sure LANGUAGES is available
        'available_languages': settings.LANGUAGES,
    }

