from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns(
    'apps.core.views',
    url('^$', 'index', name='index'),
)
