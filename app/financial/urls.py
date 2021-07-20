from django.urls import path, include

from .views import *
from .rest_views import *

app_name = 'financial'

rest_api_patterns = ([
    path('asset/add/', rest_add_asset),
    path('asset/list/', rest_list_asset),
], 'restfinancial')

urlpatterns = [
    path('api/rest/', include(rest_api_patterns))
]