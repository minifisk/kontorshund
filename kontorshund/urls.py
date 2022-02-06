
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url


urlpatterns = [
    # Django admin
    path('u86013215/', admin.site.urls),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),

    # User management
    path('accounts/', include('allauth.urls')),

    # Local apps
    path('', include('accounts.urls')),
    path('', include('core.urls')),
   # path('__debug__/', include('debug_toolbar.urls')),
    url(r'^silk/', include('silk.urls', namespace='silk')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

