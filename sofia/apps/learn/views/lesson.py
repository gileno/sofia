import datetime

from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from apps.learn.models import Project, Module, Lesson
from apps.learn.views.mixins import EnrollmentPermissionMixin


class ModuleListView(EnrollmentPermissionMixin, generic.ListView):

    template_name = 'learn/internal/modules.html'

    def get_queryset(self):
        queryset = self.get_project().modules.all()
        if not self.enrollment.is_staff:
            queryset = queryset.filter(
                release_date__isnull=False,
                release_date__gte=datetime.date.today()
            )
        return queryset


class LessonDetailView(EnrollmentPermissionMixin, generic.DetailView):

    template_name = 'learn/internal/lesson.html'
    slug_url_kwarg = 'lesson'

    def get_queryset(self):
        project = self.get_project()
        module_slug = self.kwargs.get('module')
        if self.enrollment.is_staff:
            module = get_object_or_404(project.modules.all(), slug=module_slug)
        else:
            available_modules = project.modules.filter(
                release_date__isnull=False,
                release_date__gte=datetime.date.today()
            )
            module = get_object_or_404(available_modules, slug=module_slug)
        return module.lessons.all()


module_list = login_required(ModuleListView.as_view())
lesson_detail = login_required(LessonDetailView.as_view())
