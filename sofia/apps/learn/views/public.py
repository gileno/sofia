from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.db import models

from apps.learn.models import Project, Area, Enrollment


class ProjectListView(generic.ListView):

    template_name = 'learn/project_list.html'

    _area = None

    def get_area(self):
        if self._area is None:
            area = self.kwargs.get('area', None)
            if area:
                self._area = get_object_or_404(Area, slug=area)
        return self._area

    def get_tag(self):
        return self.kwargs.get('tag', None)

    def get_queryset(self):
        area = self.get_area()
        if area:
            queryset = area.projects.all()
        else:
            queryset = Project.objects.all()
        tag = self.get_tag()
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        q = self.request.GET.get('q', None)
        if q:
            queryset = queryset.filter(
                models.Q(name__icontains=q) |
                models.Q(description__icontains=q) |
                models.Q(area__name__icontains=q) |
                models.Q(tags__name__icontains=q)
            ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['current_area'] = self.get_area()
        context['tag'] = self.get_tag()
        return context


class ProjectDetailView(generic.DetailView):

    model = Project
    template_name = 'learn/project_detail.html'


class ProjectEnrollmentView(generic.View):

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, slug=kwargs.get('slug'))
        if request.user == project.leader:
            response = redirect('learn:project_home', project.slug)
            messages.info(
                request,
                _('Você é o líder do projeto, não necessita de inscrição')
            )
        elif project.open_enrollment:
            enrollment, created = Enrollment.objects.get_or_create(
                user=request.user, project=project
            )
            if project.already_started():
                response = redirect('learn:project_home', project.slug)
                if not created:
                    messages.info(
                        request, _('Você já está inscrito neste projeto')
                    )
                else:
                    messages.success(
                        request, _('Você foi inscrito no projeto com sucesso')
                    )
            else:
                response = redirect('accounts:dashboard')
                messages.info(request, _('Aguarde o início do projeto'))
        else:
            response = redirect(project.get_absolute_url())
            messages.error(
                request, _('As inscrições para este projeto não estão abertas')
            )
        return response


project_list = ProjectListView.as_view()
project_detail = ProjectDetailView.as_view()
project_enrollment = login_required(ProjectEnrollmentView.as_view())
