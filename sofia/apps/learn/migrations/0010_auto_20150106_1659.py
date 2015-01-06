# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0009_announcement_fixed'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='release_date',
            field=models.DateField(null=True, verbose_name='Data de Liberação', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='material',
            name='file',
            field=models.FileField(help_text='Utilizado para os tipos "Vídeo" e "Documento", para vídeos use o formato mp4', upload_to='lessons/materials', null=True, verbose_name='Arquivo', blank=True),
            preserve_default=True,
        ),
    ]
