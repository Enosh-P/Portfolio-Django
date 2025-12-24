"""
Utility functions for language handling
"""
from django.conf import settings

def get_language_from_request(request):
    """
    Get language from request (URL parameter, session, or default)
    Returns valid language code: 'en', 'de', or 'ta'
    """
    # Check URL parameter first
    lang = request.GET.get('lang', None)
    
    # Check session
    if not lang:
        lang = request.session.get('language', None)
    
    # Validate and default to 'en'
    valid_languages = [code for code, _ in settings.LANGUAGES]
    if lang not in valid_languages:
        lang = 'en'
    
    return lang

def set_language_in_session(request, language):
    """
    Store language preference in session
    """
    valid_languages = [code for code, _ in settings.LANGUAGES]
    if language in valid_languages:
        request.session['language'] = language
        return True
    return False

def get_language_field_name(field_base, language):
    """
    Get language-specific field name
    e.g., get_language_field_name('name', 'de') -> 'name_de'
    """
    return f"{field_base}_{language}"

