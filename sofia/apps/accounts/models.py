import re
import os
import hashlib
import random
import string

from django.db import models
from django.core import validators
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.auth.models import (
    AbstractBaseUser, UserManager, PermissionsMixin
)
from django.utils.http import int_to_base36
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from apps.core.models import BaseModel


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        _('Usuário'), max_length=30, unique=True, validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                _(
                    'Informe um nome de usuário válido. '
                    'Este valor deve conter apenas letras, números '
                    'e os caracteres: @/./+/-/_ .'
                ), 'invalid'
            )
        ], blank=True,
    )
    name = models.CharField(_('Nome'), max_length=100)
    email = models.EmailField(_('E-mail'), unique=True)
    verified_email = models.BooleanField(
        _('E-mail verificado'), blank=True, default=False
    )
    is_staff = models.BooleanField(_('Equipe'), default=False)
    is_active = models.BooleanField(_('Ativo'), default=True)
    date_joined = models.DateTimeField(_('Data de Entrada'), auto_now_add=True)
    about = models.TextField(_('Sobre'), blank=True)
    location = models.CharField(_('Localização'), max_length=255, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __unicode__(self):
        return self.name or self.username

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name.split(" ")[0]

    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')


class ResetPassword(BaseModel):

    user = models.ForeignKey(
        User, verbose_name=_('Usuário'), related_name='resets'
    )
    key = models.CharField(_('Chave de confirmação'), unique=True, max_length=100)
    confirmed_on = models.DateTimeField(
        _('Confirmado em'), null=True, blank=True
    )

    def send_mail(self):
        pass

    def __unicode__(self):
        return 'Nova senha para {0}'.format(self.user)

    def save(self, *args, **kwargs):
        if not self.key:
            chars = string.ascii_uppercase + string.digits
            salt = self.user.email
            random_str = ''.join([random.choice(chars) for x in range(5)])
            self.key = hashlib.sha224(random_str + salt).hexdigest()[:100]
        return super(ResetPassword, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Nova Senha')
        verbose_name_plural = _('Nova Senha')


def pre_save_user(sender, instance, **kwargs):
    if not instance.username:
        username = slugify(instance.name)[:28]
        index = 1
        while(User.objects.filter(username=username).exists()):
            username = '{0}-{1}'.format(username, index)
            index = index + 1
        instance.username = username
models.signals.pre_save.connect(
    pre_save_user, sender=User, dispatch_uid='pre_save_user'
)
