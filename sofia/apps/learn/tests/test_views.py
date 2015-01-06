import datetime

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.conf import settings

from model_mommy import mommy

from apps.learn.models import Area, Project, Announcement, Enrollment


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
        context = response.context
        queryset = context['object_list']
        self.assertEqual(queryset.count(), 15)
        self.assertEqual(context['current_area'], None)

    def test_project_list_area(self):
        project_list_url = reverse(
            'learn:project_list_area', args=[self.area1.slug]
        )
        response = self.client.get(project_list_url)
        context = response.context
        queryset = context['object_list']
        self.assertEqual(queryset.count(), 10)
        self.assertEqual(context['current_area'], self.area1)

    def test_project_list_tag(self):
        project_list_url = reverse(
            'learn:project_list_tag', args=['python']
        )
        response = self.client.get(project_list_url)
        context = response.context
        queryset = context['object_list']
        self.assertEqual(queryset.count(), 15)
        project_list_url = reverse(
            'learn:project_list_tag', args=['test']
        )
        response = self.client.get(project_list_url)
        context = response.context
        queryset = context['object_list']
        self.assertEqual(queryset.count(), 10)
        self.assertTrue(context['tag'], 'test')


class ProjectEnrollmentViewTestCase(TestCase):

    def setUp(self):
        User = get_user_model()
        self.student = mommy.prepare(User, is_active=True)
        self.student.set_password('123')
        self.student.save()
        self.leader = mommy.prepare(User, is_active=True)
        self.leader.set_password('123')
        self.leader.save()
        self.project = mommy.make(
            Project, leader=self.leader, open_enrollment=True
        )

    def tearDown(self):
        self.student.delete()
        self.project.delete()
        self.leader.delete()

    def test_project_enrollment_student(self):
        project_enrollment_url = reverse(
            'learn:project_enrollment', args=[self.project.slug]
        )
        response = self.client.get(project_enrollment_url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.student.username, password='123')
        response = self.client.get(project_enrollment_url, follow=True)
        self.assertTrue(
            Enrollment.objects.filter(
                user=self.student, project=self.project
            ).exists()
        )
        dashboard_url = reverse('accounts:dashboard')
        redirect_to, status_code = response.redirect_chain[-1]
        self.assertEqual(status_code, 302)
        self.assertTrue(redirect_to.endswith(dashboard_url))

        self.project.start_date = datetime.date.today()
        self.project.save()
        response = self.client.get(project_enrollment_url, follow=True)
        project_home_url = reverse(
            'learn:project_home', args=[self.project.slug]
        )
        redirect_to, status_code = response.redirect_chain[-1]
        self.assertEqual(status_code, 302)
        self.assertTrue(redirect_to.endswith(project_home_url))

        self.project.open_enrollment = False
        self.project.save()
        response = self.client.get(project_enrollment_url, follow=True)
        redirect_to, status_code = response.redirect_chain[-1]
        self.assertEqual(status_code, 302)
        self.assertTrue(redirect_to.endswith(self.project.get_absolute_url()))


class ProjectHomeViewTestCase(TestCase):

    def setUp(self):
        User = get_user_model()
        self.student = mommy.prepare(User, is_active=True)
        self.student.set_password('123')
        self.student.save()
        self.leader = mommy.prepare(User, is_active=True)
        self.leader.set_password('123')
        self.leader.save()
        self.superuser = mommy.prepare(
            User, is_active=True, is_superuser=True, is_staff=True
        )
        self.superuser.set_password('123')
        self.superuser.save()
        self.project1 = mommy.make(Project, leader=self.leader)
        self.project2 = mommy.make(Project)
        self.announcements_project1 = mommy.make(
            Announcement, project=self.project1, fixed=False, _quantity=5
        )
        self.announcements_project2 = mommy.make(
            Announcement, project=self.project2, fixed=False, _quantity=10
        )
        self.enrollment = mommy.make(
            Enrollment, project=self.project1, user=self.student,
            blocked=True
        )
        self.client = Client()

    def tearDown(self):
        self.project1.delete()
        self.project2.delete()
        self.student.delete()
        self.leader.delete()
        self.superuser.delete()
        self.client.logout()

    def test_project_home_access_leader(self):
        self.client.login(username=self.leader.username, password='123')
        project_home_url = reverse(
            'learn:project_home', args=[self.project1.slug]
        )
        response = self.client.get(project_home_url)
        self.assertEqual(response.status_code, 200)

        project_home_url = reverse(
            'learn:project_home', args=[self.project2.slug]
        )
        response = self.client.get(project_home_url)
        self.assertEqual(response.status_code, 403)

    def test_project_home_access_student(self):
        self.client.login(username=self.student.username, password='123')
        project_home_url = reverse(
            'learn:project_home', args=[self.project1.slug]
        )
        response = self.client.get(project_home_url)
        self.assertEqual(response.status_code, 302)

        self.project1.start_date = datetime.date.today()
        self.project1.save()
        response = self.client.get(project_home_url)
        self.assertEqual(response.status_code, 403)

        self.enrollment.blocked = False
        self.enrollment.save()
        response = self.client.get(project_home_url)
        self.assertEqual(response.status_code, 200)

        project_home_url = reverse(
            'learn:project_home', args=[self.project2.slug]
        )
        response = self.client.get(project_home_url)
        self.assertEqual(response.status_code, 403)

    def test_project_home_access_superuser(self):
        self.client.login(username=self.superuser.username, password='123')
        project_home_url = reverse(
            'learn:project_home', args=[self.project1.slug]
        )
        response = self.client.get(project_home_url)
        self.assertEqual(response.status_code, 200)

        project_home_url = reverse(
            'learn:project_home', args=[self.project2.slug]
        )
        response = self.client.get(project_home_url)
        self.assertEqual(response.status_code, 200)

    def test_project_home_announcements(self):
        self.client.login(username=self.superuser.username, password='123')

        project_home_url = reverse(
            'learn:project_home', args=[self.project1.slug]
        )
        response = self.client.get(project_home_url)
        queryset = response.context['object_list']
        paginator = response.context['paginator']
        self.assertEqual(queryset.count(), 5)
        self.assertEqual(paginator.num_pages, 1)

        project_home_url = reverse(
            'learn:project_home', args=[self.project2.slug]
        )
        response = self.client.get(project_home_url)
        queryset = response.context['object_list']
        paginator = response.context['paginator']
        self.assertEqual(queryset.count(), 5)
        self.assertEqual(paginator.num_pages, 2)
