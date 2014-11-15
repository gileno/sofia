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
from django.core import validators
from django.core.urlresolvers import reverse


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        _('Username'), max_length=30, unique=True, validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'), 
                _('Enter a valid username. '
                'This value may contain only letters, numbers '
                'and @/./+/-/_ characters.'), 'invalid'
            )
        ], blank=True,
    )
    name = models.CharField(_('Name'), max_length=100)
    email = models.EmailField(_('E-mail'), unique=True)
    verified_email = models.BooleanField(
        _('Verified e-mail'), blank=True, default=False
    )
    is_staff = models.BooleanField(_('Staff'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)
    date_joined = models.DateTimeField(_('Date joined'), auto_now_add=True)
    about = models.TextField(_('Bio'), blank=True)
    location = models.CharField(_('Location'), max_length=255, blank=True)

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
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class ResetPassword(models.Model):

    user = models.ForeignKey(
        User, verbose_name=_('User'), related_name='resets'
    )
    key = models.CharField(_('Confirmation key'), unique=True, max_length=100)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    confirmed_on = models.DateTimeField(_('Confirmed on'), null=True, blank=True)

    def send_mail(self):
        context = {
            'user': self.user,
            'reset_url': reverse('set_password', args=[self.key])
        }
        subject = _('Reset password')

    def __unicode__(self):
        return 'Reset password for {0}'.format(self.user)

    def save(self, *args, **kwargs):
        if not self.key:
            chars = string.ascii_uppercase + string.digits
            salt = self.user.email
            random_str = ''.join([random.choice(chars) for x in xrange(5)])
            self.key = hashlib.sha224(random_str + salt).hexdigest()[:100]
        return super(ResetPassword, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Reset Password')
        verbose_name_plural = _('Reset Passwords')


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
