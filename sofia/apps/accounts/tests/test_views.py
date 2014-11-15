from django.test import TestCase
from django.test.client import RequestFactory, Client
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import authenticate

from model_mommy import mommy

from apps.accounts.models import User, ResetPassword
