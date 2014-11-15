from django.test import SimpleTestCase
from django.test.client import RequestFactory, Client
from django.core import mail
from django.core.urlresolvers import reverse
from django.conf import settings

from model_mommy import mommy

from apps.accounts.models import User


class UserTestCase(SimpleTestCase):

    def setUp(self):
        self.user1 = mommy.make(User, name='Fulano de Tal')
        self.user2 = mommy.make(User, name='Fulano de Tal')

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()

    def test_username_signal(self):
        self.assertEqual(self.user1.username, 'fulano-de-tal')
        self.assertEqual(self.user2.username, 'fulano-de-tal-1')
