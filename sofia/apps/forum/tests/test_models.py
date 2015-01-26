from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from model_mommy import mommy

from apps.forum.models import Topic, Reply


class TopicTestCase(TestCase):

    def setUp(self):
        self.topic = mommy.make(Topic)

    def tearDown(self):
        self.topic.delete()

    def test_update_views(self):
        self.topic.update_views()
        self.topic = Topic.objects.get(pk=self.topic.pk)
        self.assertEqual(self.topic.views, 1)


class ReplyTestCase(TestCase):

    def setUp(self):
        self.topic = mommy.make(Topic)
        self.replies = mommy.make(Reply, topic=self.topic, _quantity=10)

    def tearDown(self):
        Reply.objects.all().delete()

    def test_post_save_reply(self):
        first_reply = self.replies[0]
        first_reply.right_answer = True
        first_reply.save()
        other_replies = Reply.objects.filter(right_answer=False)
        self.assertEqual(other_replies.count(), 9)
        first_reply = Reply.objects.get(pk=first_reply.pk)
        self.assertTrue(first_reply.right_answer)
        other_reply = other_replies[0]
        other_reply.right_answer = True
        other_reply.save()
        other_replies = Reply.objects.filter(right_answer=False)
        self.assertEqual(other_replies.count(), 9)
        other_reply = Reply.objects.get(pk=other_reply.pk)
        self.assertTrue(other_reply.right_answer)
