# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(verbose_name='Criado em', auto_now_add=True)),
                ('modified', models.DateTimeField(verbose_name='Modificado em', auto_now=True)),
                ('text', models.TextField(verbose_name='Texto')),
                ('right_answer', models.BooleanField(verbose_name='Resposta Correta?', editable=False, default=False)),
                ('author', models.ForeignKey(verbose_name='Autor', to=settings.AUTH_USER_MODEL, related_name='replies_created')),
            ],
            options={
                'verbose_name': 'Resposta ao Tópico',
                'verbose_name_plural': 'Respostas aos Tópicos',
                'ordering': ['-right_answer', 'created'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('created', models.DateTimeField(verbose_name='Criado em', auto_now_add=True)),
                ('modified', models.DateTimeField(verbose_name='Modificado em', auto_now=True)),
                ('name', models.CharField(verbose_name='Nome', max_length=100)),
                ('slug', models.CharField(verbose_name='Identificador', max_length=100)),
                ('text', models.TextField(verbose_name='Texto')),
                ('views', models.IntegerField(blank=True, verbose_name='Visualizações', editable=False, default=0)),
                ('object_id', models.PositiveIntegerField(blank=True, null=True, verbose_name='Id do Objeto')),
                ('author', models.ForeignKey(verbose_name='Autor', to=settings.AUTH_USER_MODEL, related_name='topics_created')),
                ('content_type', models.ForeignKey(null=True, verbose_name='Tipo do Conteúdo', blank=True, to='contenttypes.ContentType')),
                ('followers', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Seguidores', related_name='topics_following')),
            ],
            options={
                'verbose_name': 'Tópico',
                'verbose_name_plural': 'Tópicos',
                'ordering': ['-modified'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='reply',
            name='topic',
            field=models.ForeignKey(verbose_name='Tópico', to='forum.Topic', related_name='replies'),
            preserve_default=True,
        ),
    ]
