from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from model_mommy import mommy


class IndexViewTestCase(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = mommy.prepare(User, is_active=True)
        self.user.set_password('123')
        self.user.save()
        self.client = Client()

    def tearDown(self):
        self.user.delete()

    def test_correct_redirect(self):
        project_list_url = reverse('learn:project_list')
        dashboard_url = reverse('accounts:dashboard')
        index_url = reverse('core:index')
        response = self.client.get(index_url)
        redirect_to = response.get('location')
        self.assertTrue(redirect_to.endswith(project_list_url))
        self.client.login(username=self.user.username, password='123')
        response = self.client.get(index_url)
        redirect_to = response.get('location')
        self.assertTrue(redirect_to.endswith(dashboard_url))
