from django.views import generic
from django.shortcuts import get_object_or_404

from apps.learn.models import Project, Area


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
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['current_area'] = self.get_area()
        context['tag'] = self.get_tag()
        return context


class ProjectDetailView(generic.DetailView):

    model = Project
    template_name = 'learn/project_detail.html'


project_list = ProjectListView.as_view()
project_detail = ProjectDetailView.as_view()
