from django.conf.urls import patterns, url


urlpatterns = patterns(
    'apps.accounts.views',
    # dasboard
    url(r'^$', 'dashboard', name='dashboard'),
    url(r'^dados-basicos/$', 'update_account', name='update_account'),
    # register
    url(r'^cadastro/$', 'signup', name='signup'),
    url(r'^confirmar-email/$', 'confirm_email', name='confirm_email'),
    url(
        r'^confirmar-email/(?P<pk>\d+)/(?P<token>.+)/$', 'check_email',
        name='check_email'
    ),
    # password
    url(r'^esqueceu-a-senha/$', 'reset_password', name='reset_password'),
    url(r'^nova-senha/(?P<key>.*)/$', 'set_password', name='set_password'),
    url(r'^alterar-a-senha/$', 'change_password', name='change_password'),
    # notifications
    url(r'^notificacoes/$', 'notifications', name='notifications'),
)

urlpatterns += patterns(
    '',
    url(r'^entrar/$', 'django.contrib.auth.views.login',
        {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^sair/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),
)
