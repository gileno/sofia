from django.test import TestCase
from django.core import mail
from django.test.client import RequestFactory, Client
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator

from model_mommy import mommy

from apps.accounts.models import User, ResetPassword


class SignupViewTestCase(TestCase):

    user_data = {
        'email': 'test@test.com', 'name': 'Test Name', 'password': '123'
    }

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('accounts:signup')

    def tearDown(self):
        pass

    def test_signup_ok(self):
        response = self.client.post(self.signup_url, self.user_data)
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email=self.user_data['email'])
        self.assertEqual(user.is_active, False)

    def test_signup_send_mail(self):
        self.client.post(self.signup_url, self.user_data)
        user = User.objects.get(email=self.user_data['email'])
        token = default_token_generator.make_token(user)
        check_email_url = reverse(
            'accounts:check_email', args=[user.pk, token]
        )
        exp = check_email_url in mail.outbox[0].body
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(exp)

    def test_signup_check_email(self):
        self.client.post(self.signup_url, self.user_data)
        user = User.objects.get(email=self.user_data['email'])
        token = default_token_generator.make_token(user)
        check_email_url = reverse(
            'accounts:check_email', args=[user.pk, token]
        )
        response = self.client.get(check_email_url)
        self.assertTemplateUsed(response, 'accounts/check_email.html')
        # reload
        user = User.objects.get(email=self.user_data['email'])
        self.assertTrue(user.is_active)
        self.assertTrue(user.verified_email)


class ResetPasswordTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = mommy.make(User, email='ok@test.com')
        self.reset_password_url = reverse('accounts:reset_password')

    def tearDown(self):
        self.user.delete()

    def test_reset_password_not_existing_email(self):
        data = {
            'email': 'error@test.com'
        }
        response = self.client.post(self.reset_password_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)  # confirm email

    def test_reset_password_existing_email(self):
        response = self.client.get(self.reset_password_url)
        self.assertEqual(response.status_code, 200)
        data = {
            'email': self.user.email
        }
        response = self.client.post(self.reset_password_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 2)  # confirm email
        reset_password = ResetPassword.objects.get(user=self.user)
        set_password_url = reverse(
            'accounts:set_password', args=[reset_password.key]
        )
        exp = set_password_url in mail.outbox[1].body
        self.assertTrue(exp)


class SetPasswordTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = mommy.make(User, email='ok@test.com')
        self.reset_password = mommy.make(ResetPassword, user=self.user)

    def tearDown(self):
        self.reset_password.delete()
        self.user.delete()
