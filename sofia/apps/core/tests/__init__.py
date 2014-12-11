from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse


class ContextProcessorsTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_settings_context_processor(self):
        url_index = reverse('core:index')
        response = self.client.get(url_index)
        exp = 'SITE_NAME' in response.context and \
            'SITE_DOMAIN' in response.context
        self.assertTrue(exp)
