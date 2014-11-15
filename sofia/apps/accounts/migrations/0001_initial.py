# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import re
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$', 32), 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], unique=True, verbose_name='Username', blank=True, max_length=30)),
                ('name', models.CharField(verbose_name='Name', max_length=100)),
                ('email', models.EmailField(unique=True, verbose_name='E-mail', max_length=75)),
                ('verified_email', models.BooleanField(verbose_name='Verified e-mail', default=False)),
                ('is_staff', models.BooleanField(verbose_name='Staff', default=False)),
                ('is_active', models.BooleanField(verbose_name='Active', default=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date joined')),
                ('about', models.TextField(verbose_name='Bio', blank=True)),
                ('location', models.CharField(verbose_name='Location', blank=True, max_length=255)),
                ('groups', models.ManyToManyField(verbose_name='groups', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_name='user_set', related_query_name='user', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResetPassword',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('key', models.CharField(unique=True, verbose_name='Confirmation key', max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('confirmed_on', models.DateTimeField(null=True, verbose_name='Confirmed on', blank=True)),
                ('user', models.ForeignKey(related_name='resets', verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Reset Password',
                'verbose_name_plural': 'Reset Passwords',
            },
            bases=(models.Model,),
        ),
    ]
