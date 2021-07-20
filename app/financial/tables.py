from django_tables2 import tables, Column
from django.utils.translation import gettext as _

from .models import *


class AssetTable(tables.Table):

    class Meta:
        model = Asset
        attrs = {
            'class': 'table table-striped table-hover table-vcenter card-table'
        }
        row_attrs = {'class': 'text-muted'}
        per_page = 20
        fields = ['name', 'modality']


class ApplianceTable(tables.Table):

    total = Column(verbose_name=_("Total"), accessor="get_total")

    class Meta:
        model = Appliance
        attrs = {
            'class': 'table table-striped table-hover table-vcenter card-table'
        }
        row_attrs = {'class': 'text-muted'}
        per_page = 20
        fields = ['asset', 'request_date', 'quantity',
                  'unit_price', 'total', 'ip_address']


class RedeemTable(tables.Table):

    total = Column(verbose_name=_("Total"), accessor="get_total")

    class Meta:
        model = Redeem
        attrs = {
            'class': 'table table-striped table-hover table-vcenter card-table'
        }
        row_attrs = {'class': 'text-muted'}
        per_page = 20
        fields = ['asset', 'request_date', 'quantity',
                  'unit_price', 'total', 'ip_address']
