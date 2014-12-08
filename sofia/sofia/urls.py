from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns(
    '',
    url(r'^', include('apps.core.urls', namespace='core')),
    url(r'^accounts/', include('apps.accounts.urls', namespace='accounts')),
    url(r'^admin/', include(admin.site.urls)),
)

handler500 = 'apps.core.views.error500'
handler404 = 'apps.core.views.error404'

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(
            r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {
                'document_root': settings.MEDIA_ROOT,
                'show_indexes': True
            }
        ),
        url(
            r'^404/$', handler404,
        ),
        url(
            r'^500/$', handler500,
        ),
    )
