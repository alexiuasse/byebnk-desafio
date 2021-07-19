from django.conf import settings


def general_template_context(request):
    """Context data for template."""
    return {
        'NAME_OF_ENTERPRISE': settings.NAME_OF_ENTERPRISE,
        'NAME_OF_ENTERPRISE_SHORT': settings.NAME_OF_ENTERPRISE_SHORT,
        'CONTACT_EMAIL': settings.CONTACT_EMAIL,
        'VERSION': settings.VERSION,
        'FOOTER_LINK': settings.FOOTER_LINK,
        'FOOTER_TEXT': settings.FOOTER_TEXT,
        'FOOTER_COPYRIGHT': settings.FOOTER_COPYRIGHT,
        'SOURCE_CODE_LINK': settings.SOURCE_CODE_LINK,
        'DEFAULT_DECIMAL_PLACES': settings.DEFAULT_DECIMAL_PLACES,
        'DEFAULT_MAX_DIGITS': settings.DEFAULT_MAX_DIGITS,
    }
