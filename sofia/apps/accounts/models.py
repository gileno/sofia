# -*- coding: utf-8 -*-

import re
import hashlib
import random
import string

from django.db import models
from django.core import validators
from django.template.defaultfilters import slugify
from django.contrib.auth.models import (
    AbstractBaseUser, UserManager, PermissionsMixin
)
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import ugettext_lazy as _

from apps.core.models import BaseModel
from apps.core.mail import send_mail_template


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        _('Apelido / Usuário'), max_length=30, unique=True, validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                _(
                    'Informe um nome de usuário válido. '
                    'Este valor deve conter apenas letras, números '
                    'e os caracteres: @/./+/-/_ .'
                ), 'invalid'
            )
        ], help_text='Um nome curto que será usado para identificá-lo de '
        'forma única na plataforma'
    )
    name = models.CharField(_('Nome'), max_length=100)
    email = models.EmailField(_('E-mail'), unique=True)
    verified_email = models.BooleanField(
        _('E-mail verificado'), blank=True, default=False
    )
    is_staff = models.BooleanField(_('Equipe'), default=False)
    is_active = models.BooleanField(_('Ativo'), default=False)
    date_joined = models.DateTimeField(_('Data de Entrada'), auto_now_add=True)
    about = models.TextField(_('Sobre'), blank=True)
    location = models.CharField(_('Localização'), max_length=255, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name or self.username

    def save(self, *args, **kwargs):
        if not self.username:
            username = slugify(self.name)[:28]
            index = 1
            while User.objects.filter(username=username).exclude(
                pk=self.pk
            ).exists():
                username = '{0}-{1}'.format(username, index)
                index = index + 1
            self.username = username
        return super(User, self).save(*args, **kwargs)

    def send_confirm_mail(self):
        subject = 'Confirmação de E-mail'
        template_name = 'accounts/emails/confirm_mail.html'
        context = {
            'user': self, 'token': default_token_generator.make_token(self)
        }
        recipient_list = [self.email]
        send_mail_template(
            subject, template_name, context, recipient_list,
        )

    def check_email(self, token):
        if default_token_generator.check_token(self, token):
            self.verified_email = True
            self.is_active = True
            self.save()
            return True
        return False

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
    key = models.CharField(
        _('Chave de confirmação'), unique=True, max_length=100
    )
    confirmed_on = models.DateTimeField(
        _('Confirmado em'), null=True, blank=True
    )

    def send_mail(self):
        subject = 'Criar Nova Senha'
        template_name = 'accounts/emails/reset_password_mail.html'
        context = {'reset_password': self}
        recipient_list = [self.user.email]
        send_mail_template(
            subject, template_name, context, recipient_list,
        )

    def __str__(self):
        return 'Nova senha para {0}'.format(self.user)

    def save(self, *args, **kwargs):
        if not self.key:
            chars = string.ascii_uppercase + string.digits
            salt = self.user.email
            random_str = ''.join([random.choice(chars) for x in range(5)])
            hashing = random_str + salt
            hashing_str = hashing.encode('utf-8')
            self.key = hashlib.sha224(hashing_str).hexdigest()[:100]
        return super(ResetPassword, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Nova Senha')
        verbose_name_plural = _('Nova Senha')


def post_save_user(instance, created, **kwargs):
    if created:
        instance.send_confirm_mail()

models.signals.post_save.connect(
    post_save_user, sender=User, dispatch_uid='post_save_user'
)
