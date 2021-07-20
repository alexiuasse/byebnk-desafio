from django.urls import path, include

from .views import *
from .rest_views import *

app_name = 'financial'

rest_api_patterns = ([
    path('asset/add/', rest_add_asset),
    path('asset/list/', rest_list_asset),
    path('appliance/add/', rest_appliance_add),
    path('appliance/list/', rest_appliance_list),
    path('redeem/add/', rest_redeem_add),
    path('redeem/list/', rest_redeem_list),
], 'restfinancial')

asset_patterns = ([
    path('view/', AssetView.as_view(), name='view'),
], 'asset')

appliance_patterns = ([
    path('view/', ApplianceView.as_view(), name='view'),
], 'appliance')

redeem_patterns = ([
    path('view/', RedeemView.as_view(), name='view'),
], 'redeem')

urlpatterns = [
    path('api/rest/', include(rest_api_patterns)),
    path('asset/', include(asset_patterns)),
    path('appliance/', include(appliance_patterns)),
    path('redeem/', include(redeem_patterns)),

    path('appliance/dashboard/data/chart/donut/', get_appliance_data_chart_donut),
]
