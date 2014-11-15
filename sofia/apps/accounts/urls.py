from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout


urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', 
        {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', 
        {'next_page': '/'}, name='logout'),
)