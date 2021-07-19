import logging
from django.utils.translation import gettext as _
from django.shortcuts import render

logger = logging.getLogger(__name__)

# This is the errors views, you can change the messages as you wish.
# If you wanna add a new error view, you must go to app -> urls and set it.


def error_400(request, exception):
    logger.error("Error 400: [%s]" % exception)
    return render(request, 'error.html', {
        'error_code': 400,
        'error_text': _("Wrong request or corrupted."),
    }, status=400)


def error_401(request, exception):
    logger.error("Error 401: [%s]" % exception)
    return render(request, 'error.html', {
        'error_code': 401,
        'error_text': _("You don't have permission to access this page!"),
    }, status=401)


def error_403(request, exception):
    logger.error("Error 403: [%s]" % exception)
    return render(request, 'error.html', {
        'error_code': 403,
        'error_text': _("You don't have permission to access this page!"),
    }, status=403)


def error_404(request, exception):
    logger.error("Error 404: [%s]" % exception)
    return render(request, 'error.html', {
        'error_code': 404,
        'error_text': _("Page Not Found!"),
    }, status=404)


def error_500(request):
    return render(request, 'error.html', {
        'error_code': 500,
        'error_text': _("Internal Server Error!"),
    }, status=500)


def error_503(request):
    return render(request, 'error.html', {
        'error_code': 503,
        'error_text': _("Our service is not availabel at this moment!"),
    }, status=503)
