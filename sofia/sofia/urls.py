from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns(
    '',
    url(r'^', include('apps.core.urls', namespace='core')),
    url(r'^conta/', include('apps.accounts.urls', namespace='accounts')),
    url(r'^admin/basico/', include(admin.site.urls)),
    url(r'^', include('apps.learn.urls', namespace='learn')),
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
            r'^errors/404/$', handler404,
        ),
        url(
            r'^errors/500/$', handler500,
        ),
    )
