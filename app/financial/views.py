from django.http.response import JsonResponse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from app.mixins import MyViewCreateMixin

from .forms import *
from .tables import *
from .filters import *
from .models import *
from .utils import *


class AssetView(MyViewCreateMixin):
    model_class = Asset
    form_class = AssetForm
    form_prefix = "assetform"
    table_class = AssetTable
    filterset_class = AssetFilter
    template_name = "financial/asset/view.html"
    page_title = _("Asset")
    page_title_icon = "file_invoice"
    success_url = reverse_lazy('financial:asset:view')
    permission_required = ('financial.view_asset', 'financial.add_asset')

    def get_POST_data(self):
        data = self.request.POST.copy()
        data[f"{self.form_prefix}-user"] = self.request.user.pk
        return data


class ApplianceView(MyViewCreateMixin):
    model_class = Appliance
    form_class = ApplianceForm
    form_prefix = "applianceform"
    table_class = ApplianceTable
    filterset_class = ApplianceFilter
    template_name = "financial/appliance/view.html"
    page_title = _("Appliance")
    page_title_icon = "file_invoice"
    success_url = reverse_lazy('financial:appliance:view')
    permission_required = ('financial.view_appliance',
                           'financial.add_appliance')

    def get_filterset_queryset(self):
        """Return the filter queryset, it may be used as data to a table."""
        filterset = self.get_filterset()
        # filter the queryset to send only the objects from the user
        return filterset.qs.filter(user=self.request.user)

    def get_POST_data(self):
        data = self.request.POST.copy()
        data[f"{self.form_prefix}-user"] = self.request.user.pk
        data[f"{self.form_prefix}-ip_address"] = get_client_ip(self.request)
        return data


class RedeemView(MyViewCreateMixin):
    model_class = Redeem
    form_class = RedeemForm
    form_prefix = "redeemform"
    table_class = RedeemTable
    filterset_class = RedeemFilter
    template_name = "financial/redeem/view.html"
    page_title = _("Redeem")
    page_title_icon = "file_invoice"
    success_url = reverse_lazy('financial:redeem:view')
    permission_required = ('financial.view_redeem', 'financial.add_redeem')

    def get_filterset_queryset(self):
        """Return the filter queryset, it may be used as data to a table."""
        filterset = self.get_filterset()
        # filter the queryset to send only the objects from the user
        return filterset.qs.filter(user=self.request.user)

    def get_POST_data(self):
        data = self.request.POST.copy()
        data[f"{self.form_prefix}-user"] = self.request.user.pk
        data[f"{self.form_prefix}-ip_address"] = get_client_ip(self.request)
        return data


@login_required
@require_http_methods(['GET'])
@permission_required('financial.view_appliance')
def get_appliance_data_chart_donut(request):
    """Return JsonReponse with appliance separeted by asset."""
    financialMixin = FinancialMixin(request)
    return JsonResponse(financialMixin.get_appliance_by_asset_donut_chart())
