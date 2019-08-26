from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from .views import home

admin.autodiscover()

urlpatterns = [
    # Examples:
    path('', home, name='home'),
    # path('app/', include('apps.app.urls')),
    path('api/', include('schedulesy.apps.ade_api.urls', namespace='api')),
    path('legacy/', include('schedulesy.apps.ade_legacy.urls', namespace='legacy')),

    path('admin/', admin.site.urls),
]

# debug toolbar for dev
if settings.DEBUG and 'debug_toolbar'in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
