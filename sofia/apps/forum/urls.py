from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.forum.views',
    url(r'^$', 'index', name='index'),
    url(r'^tags/(?P<tag>[\w_-]+)/$', 'index', name='tagged'),
)
