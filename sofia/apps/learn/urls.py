from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns(
    'apps.learn.views.public',
    url('^projetos/$', 'project_list', name='project_list'),
)
