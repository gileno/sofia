from django.test import TestCase
from django.core import mail
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate
from django.contrib.auth.forms import SetPasswordForm

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
        data = {'email': self.user.email}
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

    def test_set_password_ok(self):
        set_password_url = reverse(
            'accounts:set_password', args=[self.reset_password.key]
        )
        response = self.client.get(set_password_url)
        self.assertTemplateUsed(response, 'accounts/set_password.html')
        data = {'new_password1': '123', 'new_password2': '123'}
        response = self.client.post(set_password_url, data)
        self.assertEqual(response.status_code, 302)
        user = authenticate(username=self.user.username, password='123')
        self.assertEqual(self.user, user)

    def test_set_password_error(self):
        set_password_url = reverse(
            'accounts:set_password', args=[self.reset_password.key]
        )
        data = {'new_password1': '123', 'new_password2': '1234'}
        response = self.client.post(set_password_url, data)
        self.assertTemplateUsed(response, 'accounts/set_password.html')


class ChangePasswordTestCase(TestCase):

    USER_PASSWORD = '123'

    def setUp(self):
        self.client = Client()
        self.user_with_password = mommy.prepare(User, is_active=True)
        self.user_with_password.set_password(self.USER_PASSWORD)
        self.user_with_password.save()
        self.user_without_password = mommy.make(User, is_active=True)
        self.change_password_url = reverse('accounts:change_password')

    def tearDown(self):
        self.user_with_password.delete()
        self.user_without_password.delete()

    def test_user_with_password(self):
        self.client.login(
            username=self.user_with_password.username,
            password=self.USER_PASSWORD
        )
        response = self.client.get(self.change_password_url)
        self.assertTemplateUsed(response, 'accounts/change_password.html')
        data = {
            'new_password1': '1234', 'new_password2': '1234',
            'old_password': '1234'
        }
        response = self.client.post(self.change_password_url, data)
        form = response.context['form']
        exp = len(form.errors) > 0
        self.assertTrue(exp)
        data['old_password'] = self.USER_PASSWORD
        response = self.client.post(self.change_password_url, data)
        exp = 'success' in response.context
        self.assertTrue(exp)

    def test_user_without_password(self):
        self.user_without_password.set_password(self.USER_PASSWORD)  # login
        self.user_without_password.save()
        self.client.login(
            username=self.user_without_password.username,
            password=self.USER_PASSWORD
        )
        self.user_without_password.set_unusable_password()
        response = self.client.get(self.change_password_url)
        form = response.context['form']
        self.assertTrue(isinstance(form, SetPasswordForm))
