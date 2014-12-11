from django.test import TestCase

from model_mommy import mommy

from apps.accounts.models import User


class UserTestCase(TestCase):

    def setUp(self):
        self.user1 = mommy.prepare(User, name='Fulano de Tal', username='')
        self.user2 = mommy.prepare(User, name='Fulano de Tal', username='')
        self.user1.save()
        self.user2.save()

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()

    def test_username_signal(self):
        self.assertEqual(self.user1.username, 'fulano-de-tal')
        self.assertEqual(self.user2.username, 'fulano-de-tal-1')
