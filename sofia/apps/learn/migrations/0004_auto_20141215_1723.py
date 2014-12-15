# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('learn', '0003_project_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('slug', models.SlugField(max_length=100, verbose_name='Identificador')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', verbose_name='Tags', through='taggit.TaggedItem', to='taggit.Tag')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Área de Estudo',
                'verbose_name_plural': 'Áreas de Estudo',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='project',
            name='area',
            field=models.ForeignKey(verbose_name='Área', blank=True, related_name='projects', null=True, to='learn.Area'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='open_enrollment',
            field=models.BooleanField(default=False, verbose_name='Inscrições Abertas'),
            preserve_default=True,
        ),
    ]
