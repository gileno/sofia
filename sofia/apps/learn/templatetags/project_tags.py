from django import template

from apps.learn.models import Enrollment, Project, Area

register = template.Library()


@register.assignment_tag
def my_projects(user):
    enrollments = Enrollment.objects.filter(user=user, blocked=False)
    return Project.objects.filter(pk__in=enrollments.values_list('project'))


@register.assignment_tag
def get_areas():
    return Area.objects.all()
