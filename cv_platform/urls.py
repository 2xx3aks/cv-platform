"""
URL configuration for CV Platform project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.http import HttpResponseRedirect
from django.utils import translation
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Language switching should be CSRF exempt (like Django's built-in view)
@require_http_methods(["POST"])
def custom_set_language(request):
    """
    Custom set_language view that ensures proper redirect and language activation.
    Prevents caching to ensure language applies immediately.
    """
    from django.urls import reverse
    from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
    
    language = request.POST.get('language')
    next_url = request.POST.get('next', request.META.get('HTTP_REFERER', '/'))
    
    # Clean up next_url - remove any existing language prefix
    if next_url:
        parsed = urlparse(next_url)
        # Remove language prefix from path (e.g., /ar/accounts/login/ -> /accounts/login/)
        path_parts = parsed.path.strip('/').split('/')
        if path_parts and path_parts[0] in [lang[0] for lang in settings.LANGUAGES]:
            # Remove language prefix
            path_parts = path_parts[1:]
        clean_path = '/' + '/'.join(path_parts) if path_parts else '/'
        
        # Remove language parameters from query string
        if parsed.query:
            params = parse_qs(parsed.query)
            params.pop('lang', None)
            params.pop('language', None)
            new_query = urlencode(params, doseq=True)
        else:
            new_query = ''
        
        next_url = urlunparse((parsed.scheme, parsed.netloc, clean_path, parsed.params, new_query, parsed.fragment))
    
    # Validate language
    if language and language in [lang[0] for lang in settings.LANGUAGES]:
        # Activate language immediately
        translation.activate(language)
        
        # Store in session
        request.session['django_language'] = language
        request.session.modified = True
        request.session.save()  # Force save
        
        # Add language prefix to next_url if using i18n_patterns
        # With prefix_default_language=False, default language doesn't need prefix
        if next_url and next_url.startswith('/') and not next_url.startswith('/static/') and not next_url.startswith('/media/') and not next_url.startswith('/i18n/'):
            # Check if URL already has a language prefix
            path_parts = next_url.strip('/').split('/')
            has_lang_prefix = path_parts and path_parts[0] in [lang[0] for lang in settings.LANGUAGES]
            
            # Add language prefix only if needed and not default language
            if not has_lang_prefix:
                # Only add prefix for non-default languages
                # Default language works without prefix when prefix_default_language=False
                if language != settings.LANGUAGE_CODE:
                    next_url = f'/{language}{next_url}'
        
        # Create response with cache-busting headers
        response = HttpResponseRedirect(next_url)
        
        # Prevent caching
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        
        # Set cookie - use explicit name
        cookie_name = getattr(settings, 'LANGUAGE_COOKIE_NAME', 'django_language')
        # Delete old cookie first to ensure it's updated
        response.delete_cookie(cookie_name, path='/')
        # Set new cookie
        response.set_cookie(
            cookie_name,
            language,
            max_age=365*24*60*60,  # 1 year
            path='/',
            domain=None,  # Use default domain
            samesite='Lax',
            httponly=False,  # Allow JavaScript access if needed
            secure=False  # Set to True in production with HTTPS
        )
        
        return response
    
    # Fallback to default
    response = HttpResponseRedirect(next_url)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

urlpatterns = [
    # Use custom set_language for better control
    path('i18n/setlang/', custom_set_language, name='set_language'),
    path('i18n/', include('django.conf.urls.i18n')),
]

# No root redirect needed - i18n_patterns handles root URL automatically

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('cv_extraction.urls')),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

