from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@require_http_methods(["GET"])
def index(request):
    """
    Index that redirects to dashboard if authenticated and if it is superuser, else redirect to login page. If not authenticated redirect to login to (maybe you wanna put a homepage?)
    """
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return HttpResponseRedirect(reverse('dashboard:dashboard'))
        else:
            return HttpResponseRedirect(reverse('login'))
    else:
        # return HttpResponseRedirect(reverse('homepage'))
        return HttpResponseRedirect(reverse('login'))


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@require_http_methods(["GET"])
def error_test_view(request):
    """Just a view to test error template."""
    return render(request, template_name="error.html", context={'error_code': 404, 'error_text': 'Page not found!'})
