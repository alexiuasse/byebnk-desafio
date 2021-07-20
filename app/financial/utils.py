from django.db.models import Sum
from django.conf import settings
from .models import *


def get_client_ip(request):
    """Return the client ip"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # the real client ip is the last one
        ip = x_forwarded_for.split(',')[-1]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class FinancialMixin:
    appliances = None
    redeems = None
    request = None

    def __init__(self, request=None):
        if request is not None:
            self.request = request

    def get_appliances(self):
        """Return all appliance from current user."""
        if self.appliances is not None:
            return self.appliances
        self.appliances = Appliance.objects.filter(user=self.request.user)
        return self.appliances

    def get_redeems(self):
        """Return all redeem from current user."""
        if self.redeems is not None:
            return self.redeems
        self.redeems = Redeem.objects.filter(user=self.request.user)
        return self.redeems

    def get_total_appliance(self):
        """Return the total appliances."""
        total = 0
        for appliance in self.get_appliances():
            total += appliance.get_total()
        return total

    def get_total_redeem(self):
        """Return the total redeems."""
        total = 0
        for redeem in self.get_redeems():
            total += redeem.get_total()
        return total

    def get_appliance_by_asset_donut_chart(self):
        """
        Return appliance separeted by asset in Json format for a donut chart.
        """
        appliances = self.get_appliances().order_by('asset')
        assets = Asset.objects.filter(
            pk__in=[a['asset'] for a in appliances.values('asset').distinct()]
        )
        data = {
            'series': [],
            'labels': [asset.name for asset in assets],
        }
        for asset in assets:
            _appliances = appliances.filter(asset=asset)
            _total = 0
            for appliance in _appliances:
                _total += float(
                    round(
                        appliance.total or 0, settings.DEFAULT_DECIMAL_PLACES
                    )
                )
            data['series'].append(_total)
        return data
