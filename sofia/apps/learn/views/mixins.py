from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from apps.learn.models import Project


class EnrollmentPermissionMixin(object):

    context_project_name = 'project'
    _project = None
    enrollment = None

    def get_project(self):
        if self._project is None:
            slug = self.kwargs.get('slug')
            self._project = get_object_or_404(Project, slug=slug)
        return self._project

    def dispatch(self, request, *args, **kwargs):
        project = self.get_project()
        ok, self.enrollment = project.has_access_permission(request.user)
        if not ok:
            if self.enrollment and not project.already_started():
                messages.info(request, _('Aguarde o início do projeto'))
                return redirect('accounts:dashboard')
            else:
                raise PermissionDenied
        return super(EnrollmentPermissionMixin, self).dispatch(
            request, *args, **kwargs
        )

    def get_context_data(self, **kwargs):
        context = super(EnrollmentPermissionMixin, self).get_context_data(
            **kwargs
        )
        context['enrollment'] = self.enrollment
        return context
