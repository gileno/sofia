"""
Django settings for project_name project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9zks7*6*++sog+8o^1#*o(ydu&v@tdm02q204*f_n5$4)i66o!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'suit',
    # contrib
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # libs
    'gunicorn',
    'widget_tweaks',
    'taggit',
    # apps
    'apps.core',
    'apps.accounts',
    'apps.learn',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sofia.urls'

WSGI_APPLICATION = 'sofia.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sofia',
        'USER': 'sofia',
        'PASSWORD': 'sofia',
        'HOST': '127.0.0.1',
    }
}

ATOMIC_REQUESTS = True

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
    'apps.core.context_processors.settings',
)

# Site settings
SITE_NAME = 'Sofia - Plataforma Educacional'
SITE_DOMAIN = 'sofiaplataforma.com.br'

# Mail Settings
DEFAULT_FROM_EMAIL = 'sistema@sofiaplataforma.com.br'
CONTEXT_EXTRA_MAIL = {
    'SITE_NAME': SITE_NAME,
    'SITE_DOMAIN': SITE_DOMAIN
}
DEFAULT_SUBJECT_PREFIX = '[SOFIA] '
DEFAULT_CONTACT_EMAIL = 'contato@sofiaplataforma.com.br'

# Auth Settings
AUTHENTICATION_BACKENDS = ('apps.accounts.backends.ModelBackend',)
AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = 'accounts:login'
LOGOUT_URL = 'accounts:logout'
LOGIN_REDIRECT_URL = 'core:index'

# Suit admin
SUIT_CONFIG = {
    'ADMIN_NAME': SITE_NAME,
}

try:
    from sofia.local_settings import *
except ImportError:
    pass
