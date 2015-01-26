from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from taggit.managers import TaggableManager

from apps.core.models import BaseModel


class Topic(BaseModel):

    title = models.CharField(_('Nome'), max_length=100)
    slug = models.CharField(_('Identificador'), max_length=100)
    text = models.TextField(_('Texto'))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('Autor'),
        related_name='topics_created'
    )
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_(u'Seguidores'),
        blank=True, related_name='topics_following'
    )
    views = models.IntegerField(
        _(u'Visualizações'), blank=True, default=0, editable=False
    )

    # object
    content_type = models.ForeignKey(
        ContentType, verbose_name=_('Tipo do Conteúdo'), null=True, blank=True
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_('Id do Objeto'), null=True, blank=True
    )
    content_object = GenericForeignKey('content_type', 'object_id')
    content_object.short_description = _('Objeto Referência')

    tags = TaggableManager(blank=True)

    def update_views(self):
        Topic.objects.filter(pk=self.pk).update(views=models.F('views') + 1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Tópico')
        verbose_name_plural = _('Tópicos')
        ordering = ['-modified']


class Reply(BaseModel):

    topic = models.ForeignKey(
        Topic, verbose_name=_('Tópico'), related_name='replies'
    )
    text = models.TextField(_('Texto'))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('Autor'),
        related_name='replies_created'
    )
    right_answer = models.BooleanField(
        _(u'Resposta Correta?'), blank=True, default=False
    )

    def __str__(self):
        return '{0} replied by {1} on {2}'.format(
            self.topic, self.author, self.created
        )

    class Meta:
        verbose_name = _('Resposta ao Tópico')
        verbose_name_plural = _('Respostas aos Tópicos')
        ordering = ['-right_answer', 'created']


def post_save_reply(instance, **kwargs):
    if instance.right_answer:
        other_replies = instance.topic.replies.exclude(pk=instance.pk)
        other_replies.update(right_answer=False)


models.signals.post_save.connect(
    post_save_reply, sender=Reply, dispatch_uid='post_save_reply'
)
