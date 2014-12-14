from django.conf import settings as django_settings


def settings(request):
    return {
        'SITE_NAME': django_settings.SITE_NAME,
        'SITE_DOMAIN': django_settings.SITE_DOMAIN,
        'DEFAULT_CONTACT_EMAIL': django_settings.DEFAULT_CONTACT_EMAIL
    }
