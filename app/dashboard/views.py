import math
from django.conf import settings
from django.db.models import Sum
from django.http.response import Http404
from django.urls.base import reverse_lazy
from django.utils.translation import gettext as _
from django_tables2 import LazyPaginator, RequestConfig
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render

from app.templatetags.currency import currency
from financial.utils import FinancialMixin

from .models import *


class DashboardView(FinancialMixin, View, LoginRequiredMixin):
    template_name = "dashboard/view.html"
    page_title = _("Dashboard")
    page_title_icon = "dashboard"
    success_url = reverse_lazy("dashboard:dashboard")

    def get_context_data(self, **kwargs):
        context = {
            'page_title': self.page_title,
            'page_title_icon': self.page_title_icon,
            'total_appliance': self.get_total_appliance(),
            'total_redeemed': self.get_total_redeem(),
        }
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
