"""
Language switching view.
"""
from django.shortcuts import redirect
from django.utils import translation
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_http_methods


@require_http_methods(["POST"])
def set_language(request):
    """Switch language."""
    language = request.POST.get('language', 'en')
    
    # Validate language
    if language not in [lang[0] for lang in settings.LANGUAGES]:
        language = settings.LANGUAGE_CODE
    
    # Activate language for current request
    translation.activate(language)
    
    # Store in session - Django's LocaleMiddleware uses 'django_language' as the key
    request.session['django_language'] = language
    request.session.modified = True  # Ensure session is saved
    
    # Get redirect URL
    redirect_url = request.META.get('HTTP_REFERER', '/')
    if not redirect_url or redirect_url == request.build_absolute_uri():
        redirect_url = '/'
    
    # Create response and set cookie
    response = redirect(redirect_url)
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME, 
        language, 
        max_age=365*24*60*60,
        path='/',
        samesite='Lax'
    )
    
    return response

