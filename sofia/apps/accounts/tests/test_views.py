from django.test import TestCase
from django.test.client import RequestFactory, Client
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import authenticate

from model_mommy import mommy

from apps.accounts.models import User, ResetPassword


class ResetPasswordTestCase(TestCase):

    TEST_EMAIL = 'test@test.com'

    def setUp(self):
        self.user = mommy.make(User, email=self.TEST_EMAIL)
        self.client = Client()

    def tearDown(self):
        self.user.delete()
        ResetPassword.objects.all().delete()

    def test_reset_password_creation(self):
        url = reverse('reset_password')
        response = self.client.post(
            url, {'email': 'wrong@wrong.com'}
        )
        reset_password_count = ResetPassword.objects.count()
        self.assertEqual(reset_password_count, 0)
        response = self.client.post(
            url, {'email': self.TEST_EMAIL}
        )
        reset_password = ResetPassword.objects.get()
        self.assertEqual(reset_password.user.pk, self.user.pk)


class SetPasswordTestCase(TestCase):

    SET_PASSWORD_TEST = '123'
    TEST_EMAIL = 'test@test.com'

    def setUp(self):
        self.user = mommy.make(User, email=self.TEST_EMAIL)
        self.reset_password = mommy.make(ResetPassword, user=self.user)
        self.client = Client()

    def tearDown(self):
        self.user.delete()
        self.reset_password.delete()

    def test_set_password_and_redirect(self):
        url = reverse('set_password', args=[self.reset_password.key])
        response = self.client.post(
            url, {
                'new_password1': self.SET_PASSWORD_TEST, 
                'new_password2': self.SET_PASSWORD_TEST
            }
        )
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL)
        user = authenticate(
            email=self.user.email, password=self.SET_PASSWORD_TEST
        )
        self.assertNotEqual(user, None)
