from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout


urlpatterns = patterns(
    'apps.accounts.views',
    url(r'^cadastro/$', 'signup', name='signup'),
    url(r'^confirmar-email/$', 'confirm_email', name='confirm_email'),
    url(
        r'^confirmar-email/(?P<pk>\d+)/(?P<token>.+)/$', 'check_email',
        name='check_email'
    ),
    url(r'^esqueceu-a-senha/$', 'reset_password', name='reset_password'),
    url(r'^nova-senha/(?P<key>.*)/$', 'set_password', name='set_password'),
)

urlpatterns += patterns(
    '',
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),
)
