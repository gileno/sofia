from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from model_mommy import mommy

from apps.learn.models import Area, Project


class ProjectListViewTestCase(TestCase):

    def setUp(self):
        self.area1 = mommy.make(Area)
        self.area2 = mommy.make(Area)
        self.projects_area1 = mommy.make(
            Project, area=self.area1, _quantity=10
        )
        self.projects_area2 = mommy.make(
            Project, area=self.area2, _quantity=5
        )
        for project in self.projects_area1:
            project.tags.add("python", "test")
            project.save()
        for project in self.projects_area2:
            project.tags.add("python")
            project.save()
        self.client = Client()

    def tearDown(self):
        Project.objects.filter(area=self.area1).delete()
        Project.objects.filter(area=self.area2).delete()
        self.area1.delete()
        self.area2.delete()

    def test_project_list(self):
        project_list_url = reverse('learn:project_list')
        response = self.client.get(project_list_url)
        context = response.context_data
        queryset = context['object_list']
        self.assertEqual(queryset.count(), 15)
        self.assertEqual(context['current_area'], None)

    def test_project_list_area(self):
        project_list_url = reverse(
            'learn:project_list_area', args=[self.area1.slug]
        )
        response = self.client.get(project_list_url)
        context = response.context_data
        queryset = context['object_list']
        self.assertEqual(queryset.count(), 10)
        self.assertEqual(context['current_area'], self.area1)

    def test_project_list_tag(self):
        project_list_url = reverse(
            'learn:project_list_tag', args=['python']
        )
        response = self.client.get(project_list_url)
        context = response.context_data
        queryset = context['object_list']
        self.assertEqual(queryset.count(), 15)
        project_list_url = reverse(
            'learn:project_list_tag', args=['test']
        )
        response = self.client.get(project_list_url)
        context = response.context_data
        queryset = context['object_list']
        self.assertEqual(queryset.count(), 10)
        self.assertTrue(context['tag'], 'test')
