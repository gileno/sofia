from django import template

from apps.learn.models import Enrollment, Project

register = template.Library()


@register.assignment_tag
def my_projects(user):
    enrollments = Enrollment.objects.filter(user=user, blocked=False)
    return Project.objects.filter(pk__in=enrollments.values_list('project'))
