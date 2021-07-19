from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import index, logout_view, error_test_view

urlpatterns = [
    path('', index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'),
         name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls, name='admin'),
    path('dashboard/', include("dashboard.urls")),
    path('error/', error_test_view, name="error-test"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Handling errors, but only if debug is set to False and there is another
# server to serve staticfiles
handler400 = 'dashboard.error_views.error_400'
handler401 = 'dashboard.error_views.error_401'
handler403 = 'dashboard.error_views.error_403'
handler404 = 'dashboard.error_views.error_404'
handler500 = 'dashboard.error_views.error_500'
handler503 = 'dashboard.error_views.error_503'
