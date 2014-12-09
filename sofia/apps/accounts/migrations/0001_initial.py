# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django.core.validators
import re


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('username', models.CharField(validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$', 32), 'Informe um nome de usuário válido. Este valor deve conter apenas letras, números e os caracteres: @/./+/-/_ .', 'invalid')], unique=True, verbose_name='Usuário', blank=True, max_length=30)),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('email', models.EmailField(unique=True, verbose_name='E-mail', max_length=75)),
                ('verified_email', models.BooleanField(default=False, verbose_name='E-mail verificado')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Equipe')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Data de Entrada')),
                ('about', models.TextField(verbose_name='Sobre', blank=True)),
                ('location', models.CharField(max_length=255, verbose_name='Localização', blank=True)),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups', to='auth.Group', related_query_name='user', related_name='user_set', blank=True)),
                ('user_permissions', models.ManyToManyField(help_text='Specific permissions for this user.', verbose_name='user permissions', to='auth.Permission', related_query_name='user', related_name='user_set', blank=True)),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResetPassword',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('key', models.CharField(unique=True, verbose_name='Chave de confirmação', max_length=100)),
                ('confirmed_on', models.DateTimeField(null=True, verbose_name='Confirmado em', blank=True)),
                ('user', models.ForeignKey(related_name='resets', verbose_name='Usuário', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Nova Senha',
                'verbose_name_plural': 'Nova Senha',
            },
            bases=(models.Model,),
        ),
    ]
