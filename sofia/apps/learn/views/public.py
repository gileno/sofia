from django.views import generic

from apps.learn.models import Project


class ProjectListView(generic.ListView):

    model = Project
    template_name = 'learn/project_list.html'


project_list = ProjectListView.as_view()
