from django import template
from django.db import models

from apps.learn.models import Enrollment, Project, Area

register = template.Library()


@register.assignment_tag
def my_projects(user):
    enrollments = Enrollment.objects.filter(user=user, blocked=False)
    return Project.objects.filter(
        models.Q(pk__in=enrollments.values_list('project')) |
        models.Q(leader=user)
    )


@register.assignment_tag
def get_areas():
    return Area.objects.all()
