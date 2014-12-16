from django.conf.urls import patterns, url

urlpatterns = patterns(
    'apps.learn.views.public',
    url(r'^projetos/$', 'project_list', name='project_list'),
    url(
        r'^projetos/(?P<area>[\w_-]+)/$', 'project_list',
        name='project_list_area'
    ),
    url(
        r'^projetos/tags/(?P<tag>[\w_-]+)/$', 'project_list',
        name='project_list_tag'
    ),
    url(
        r'^(?P<slug>[\w_-]+)/$', 'project_detail', name='project_detail'
    ),
)

urlpatterns += patterns(
    'apps.learn.views.project',
    url(
        r'^(?P<slug>[\w_-]+)/inicio/$', 'project_home', name='project_home'
    ),
    url(
        r'^(?P<slug>[\w_-]+)/anuncios/(?P<announcement>[\w_-]+)/$',
        'announcement_detail', name='announcement_detail'
    ),
)
