import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.urlresolvers import reverse

from taggit.managers import TaggableManager

from apps.core.models import BaseModel

from .utils import video_info


class Area(BaseModel):

    name = models.CharField(_('Nome'), max_length=100)
    slug = models.SlugField(_('Identificador'), max_length=100)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('learn:project_list_area', args=[self.slug])

    class Meta:
        verbose_name = _('Área de Estudo')
        verbose_name_plural = _('Áreas de Estudo')
        ordering = ['name']


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
    area = models.ForeignKey(
        Area, verbose_name=_('Área'), related_name='projects', null=True,
        blank=True, on_delete=models.SET_NULL
    )
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('Líder'),
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='led_projects'
    )
    level = models.PositiveSmallIntegerField(
        _('Nível'), choices=PROJECT_LEVEL_CHOICES
    )
    # details
    description = models.TextField(_('Descrição'), blank=True)
    photo = models.ImageField(
        _('Imagem'), upload_to='projects/photos', blank=True, null=True,
        help_text=_('360x220 é a proporção ideal para a imagem')
    )
    embedded_presentation = models.TextField(
        _('Apresentação Embarcada (youtube/vimeo)'), blank=True, default='',
        help_text=_('html embarcado de uma apresentação, ex: vídeo do youtube')
    )
    # dates
    start_date = models.DateField(_('Início'), null=True, blank=True)
    end_date = models.DateField(_('Término'), null=True, blank=True)
    timeless = models.BooleanField(
        _('Atemporal'), default=False, blank=True,
        help_text=_(
            'Não tem início ou fim, pode ser acessado a qualquer momento'
        )
    )
    open_enrollment = models.BooleanField(
        _('Inscrições Abertas'), blank=True, default=False
    )

    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('learn:project_detail', args=[self.slug])

    def has_access_permission(self, user):
        if (self.leader == user) or user.is_superuser:
            enrollment = Enrollment(
                user=user, project=self, is_staff=True, blocked=False
            )
            ok = True
        else:
            try:
                enrollment = self.enrollments.get(user__pk=user.pk)
            except Enrollment.DoesNotExist:
                enrollment = None
                ok = False
            else:
                ok = (not enrollment.blocked) and (self.already_started())
        return ok, enrollment

    def already_started(self):
        today = datetime.date.today()
        return self.start_date and today >= self.start_date

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
    blocked = models.BooleanField(_('Bloqueado'), default=False, blank=True)
    is_staff = models.BooleanField(
        _('É da equipe?'), default=False, blank=True
    )

    def __str__(self):
        return '[{0}] {1}'.format(self.project, self.user)

    class Meta:
        verbose_name = _('Inscrição')
        verbose_name_plural = _('Inscrições')


class Announcement(BaseModel):

    title = models.CharField(_('Título'), max_length=100)
    slug = models.CharField(_('Identificador'), max_length=100)
    project = models.ForeignKey(
        Project, verbose_name=_('Projeto'), related_name='announcements'
    )
    fixed = models.BooleanField(
        _('Anúncio Fixo?'), blank=True, default=False
    )
    text = models.TextField(_('Mensagem'))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('Criado por'),
        related_name='announcements'
    )
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'learn:announcement_detail', args=[self.project.slug, self.slug]
        )

    class Meta:
        verbose_name = _('Anúncio')
        verbose_name_plural = _('Anúncios')
        ordering = ['-created']


class Module(BaseModel):

    name = models.CharField(_('Nome'), max_length=100)
    slug = models.CharField(_('Identificador'), max_length=100)
    project = models.ForeignKey(
        Project, verbose_name=_('Projeto'), related_name='modules'
    )
    release_date = models.DateField(
        _('Data de Liberação'), null=True, blank=True
    )
    order = models.PositiveSmallIntegerField(_('Ordem'), default=0, blank=True)
    description = models.TextField(_('Descrição'), blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'learn:module_detail', args=[module.project.slug, module.slug]
        )

    def previous(self):
        return self.project.modules.filter(
            order__lte=self.order, pk__lt=self.pk
        ).first()

    def next(self):
        return self.project.modules.filter(
            order__gte=self.order, pk__gt=self.pk
        ).first()

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

    def get_absolute_url(self):
        return reverse(
            'learn:lesson_detail',
            args=[self.module.project.slug, self.module.slug, self.slug]
        )

    def previous(self):
        prev = self.module.lessons.filter(
            order__lte=self.order, pk__lt=self.pk
        ).first()
        if prev is None:
            prev_module = self.module.previous()
            if prev_module:
                prev = prev_module.lessons.last()
        return prev

    def next(self):
        next_lesson = self.module.lessons.filter(
            order__gte=self.order, pk__gt=self.pk
        ).first()
        if next_lesson is None:
            next_module = self.module.next()
            if next_module:
                next_lesson = next_module.lessons.first()
        return next_lesson

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
        help_text=_(
            'Utilizado para os tipos "Vídeo" e "Documento", para vídeos'
            ' use o formato mp4'
        )
    )
    order = models.PositiveSmallIntegerField(
        _('Ordem'), default=0, blank=True,
        help_text=_('Ordem crescente da listagem dos materiais')
    )

    def is_youtube(self):
        if self.embedded:
            info = video_info(self.embedded)
            return info and info[1] == 'youtube'
        return False

    def is_vimeo(self):
        if self.embedded:
            info = video_info(self.embedded)
            return info and info[1] == 'vimeo'
        return False

    def downloadable(self):
        return self.material_type == self.DOCUMENT_TYPE

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Material')
        verbose_name_plural = _('Materiais')
        ordering = ['order']
