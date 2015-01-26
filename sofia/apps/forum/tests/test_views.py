from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from model_mommy import mommy

from apps.forum.models import Topic, Reply


class TopicListViewTestCase(TestCase):

    def setUp(self):
        self.topics = mommy.make(Topic, _quantity=50)
        self.client = Client()

    def tearDown(self):
        Topic.objects.all().delete()

    def test_pagination(self):
        forum_index_url = reverse('forum:index')
        response = self.client.get(forum_index_url)
        paginator = response.context_data['paginator']
        page_obj = response.context_data['page_obj']
        self.assertEqual(paginator.num_pages, 3)
        self.assertEqual(page_obj.object_list.count(), 20)
