from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from apps.learn.models import Project


class EnrollmentPermissionMixin(object):

    context_project_name = 'project'
    _project = None

    def get_project(self):
        if self._project is None:
            slug = self.kwargs.get('slug')
            self._project = get_object_or_404(Project, slug=slug)
        return self._project

    def dispatch(self, request, *args, **kwargs):
        project = self.get_project()
        if not project.has_access_permission(request.user):
            raise PermissionDenied
        return super(EnrollmentPermissionMixin, self).dispatch(
            request, *args, **kwargs
        )
