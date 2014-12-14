# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('is_staff', models.BooleanField(default=False, verbose_name='É da equipe?')),
            ],
            options={
                'verbose_name': 'Inscrição',
                'verbose_name_plural': 'Inscrições',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('slug', models.CharField(max_length=100, verbose_name='Identificador')),
                ('order', models.PositiveSmallIntegerField(default=0, blank=True, verbose_name='Ordem')),
                ('description', models.TextField(blank=True, verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Aula',
                'ordering': ['order'],
                'verbose_name_plural': 'Aulas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('material_type', models.PositiveSmallIntegerField(choices=[(0, 'Vídeo'), (1, 'Documento'), (2, 'Conteúdo Embarcado')], verbose_name='Tipo')),
                ('embedded', models.TextField(blank=True, help_text='Utilizado para o tipo "Conteúdo Embarcado"', verbose_name='Conteúdo Embarcado')),
                ('file', models.FileField(upload_to='lessons/materials', blank=True, null=True, help_text='Utilizado para os tipos "Vídeo" e "Documento"', verbose_name='Arquivo')),
                ('order', models.PositiveSmallIntegerField(default=0, blank=True, verbose_name='Ordem')),
                ('lesson', models.ForeignKey(related_name='materials', verbose_name='Aula', to='learn.Lesson')),
            ],
            options={
                'verbose_name': 'Material',
                'ordering': ['order'],
                'verbose_name_plural': 'Materiais',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('slug', models.CharField(max_length=100, verbose_name='Identificador')),
                ('order', models.PositiveSmallIntegerField(default=0, blank=True, verbose_name='Ordem')),
                ('description', models.TextField(blank=True, verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Módulo',
                'ordering': ['order'],
                'verbose_name_plural': 'Módulos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('slug', models.SlugField(max_length=100, verbose_name='Identificador')),
                ('level', models.PositiveSmallIntegerField(choices=[(0, 'Iniciante'), (1, 'Intermediário'), (2, 'Avançado')], verbose_name='Nível')),
                ('description', models.TextField(blank=True, verbose_name='Descrição')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Início')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Término')),
                ('timeless', models.BooleanField(default=False, help_text='Não tem início ou fim, pode ser acessado a qualquer momento', verbose_name='Atemporal')),
                ('leader', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True, verbose_name='Líder', related_name='led_projects', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', verbose_name='Tags', help_text='A comma-separated list of tags.')),
            ],
            options={
                'verbose_name': 'Projeto',
                'verbose_name_plural': 'Projetos',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='module',
            name='project',
            field=models.ForeignKey(related_name='modules', verbose_name='Projeto', to='learn.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lesson',
            name='module',
            field=models.ForeignKey(related_name='lessons', verbose_name='Módulo', to='learn.Module'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enrollment',
            name='project',
            field=models.ForeignKey(related_name='enrollments', verbose_name='Projeto', to='learn.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enrollment',
            name='user',
            field=models.ForeignKey(related_name='enrollments', verbose_name='Usuário', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
