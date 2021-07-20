import django_filters

from .models import *


class AssetFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="name__icontains")

    class Meta:
        model = Asset
        fields = ['name', 'modality']


class ApplianceFilter(django_filters.FilterSet):

    class Meta:
        model = Appliance
        fields = ['asset', 'request_date']


class RedeemFilter(django_filters.FilterSet):

    class Meta:
        model = Redeem
        fields = ['asset', 'request_date']
