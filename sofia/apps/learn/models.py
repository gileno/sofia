from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from taggit.managers import TaggableManager

from apps.core.models import BaseModel


class Project(BaseModel):

    BEGINNER_LEVEL = 0
    INTERMEDIATE_LEVEL = 1
    ADVANCED_LEVEL = 2

    PROJECT_LEVEL_CHOICES = (
        (BEGINNER_LEVEL, _('Iniciante')),
        (INTERMEDIATE_LEVEL, _('Intermediário')),
        (ADVANCED_LEVEL, _('Avançado')),
    )
    # basic
    name = models.CharField(_('Nome'), max_length=100)
    slug = models.SlugField(_('Identificador'), max_length=100)
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('Líder'),
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='led_projects'
    )
    level = models.PositiveSmallIntegerField(
        _('Nível'), choices=PROJECT_LEVEL_CHOICES
    )
    description = models.TextField(_('Descrição'), blank=True)
    # dates
    start_date = models.DateField(_('Início'), null=True, blank=True)
    end_date = models.DateField(_('Término'), null=True, blank=True)
    timeless = models.BooleanField(
        _('Atemporal'), default=False, blank=True,
        help_text=_(
            'Não tem início ou fim, pode ser acessado a qualquer momento'
        )
    )

    tags = TaggableManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'


class Enrollment(BaseModel):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('Usuário'),
        related_name='enrollments'
    )
    project = models.ForeignKey(
        Project, verbose_name=_('Projeto'), related_name='enrollments'
    )
    is_staff = models.BooleanField(
        _('É da equipe?'), default=False, blank=True
    )

    def __str__(self):
        return '[{0}] {1}'.format(self.project, self.user)

    class Meta:
        verbose_name = _('Inscrição')
        verbose_name_plural = _('Inscrições')


class Module(BaseModel):

    name = models.CharField(_('Nome'), max_length=100)
    slug = models.CharField(_('Identificador'), max_length=100)
    project = models.ForeignKey(
        Project, verbose_name=_('Projeto'), related_name='modules'
    )
    order = models.PositiveSmallIntegerField(_('Ordem'), default=0, blank=True)
    description = models.TextField(_('Descrição'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Módulo')
        verbose_name_plural = _('Módulos')
        ordering = ['order']


class Lesson(BaseModel):

    name = models.CharField(_('Nome'), max_length=100)
    slug = models.CharField(_('Identificador'), max_length=100)
    module = models.ForeignKey(
        Module, verbose_name=_('Módulo'), related_name='lessons'
    )
    order = models.PositiveSmallIntegerField(_('Ordem'), default=0, blank=True)
    description = models.TextField(_('Descrição'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Aula')
        verbose_name_plural = _('Aulas')
        ordering = ['order']


class Material(BaseModel):

    VIDEO_TYPE = 0
    DOCUMENT_TYPE = 1
    EMBEDDED_TYPE = 2

    MATERIAL_TYPE_CHOICES = (
        (VIDEO_TYPE, _('Vídeo')),
        (DOCUMENT_TYPE, _('Documento')),
        (EMBEDDED_TYPE, _('Conteúdo Embarcado')),
    )

    name = models.CharField(_('Nome'), max_length=100)
    lesson = models.ForeignKey(
        Lesson, verbose_name=_('Aula'), related_name='materials'
    )
    material_type = models.PositiveSmallIntegerField(
        _('Tipo'), choices=MATERIAL_TYPE_CHOICES
    )
    embedded = models.TextField(
        _('Conteúdo Embarcado'), blank=True,
        help_text=_('Utilizado para o tipo "Conteúdo Embarcado"')
    )
    file = models.FileField(
        _('Arquivo'), upload_to='lessons/materials', blank=True, null=True,
        help_text=_('Utilizado para os tipos "Vídeo" e "Documento"')
    )
    order = models.PositiveSmallIntegerField(_('Ordem'), default=0, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Material')
        verbose_name_plural = _('Materiais')
        ordering = ['order']
