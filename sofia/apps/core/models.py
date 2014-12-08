from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):

    created = models.DateTimeField(_('Criado em'), auto_now_add=True)
    modified = models.DateTimeField(_('Modificado em'), auto_now=True)
