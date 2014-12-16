# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learn', '0007_project_embedded_presentation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('title', models.CharField(max_length=100, verbose_name='Título')),
                ('slug', models.CharField(max_length=100, verbose_name='Identificador')),
                ('text', models.TextField(verbose_name='Mensagem')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='announcements', verbose_name='Criado por')),
                ('project', models.ForeignKey(to='learn.Project', related_name='announcements', verbose_name='Projeto')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', help_text='A comma-separated list of tags.', through='taggit.TaggedItem', blank=True, verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Anúncio',
                'verbose_name_plural': 'Anúncios',
                'ordering': ['-created'],
            },
            bases=(models.Model,),
        ),
    ]
