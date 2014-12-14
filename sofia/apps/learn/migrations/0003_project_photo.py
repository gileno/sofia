# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0002_auto_20141214_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='photo',
            field=models.ImageField(null=True, blank=True, upload_to='projects/photos', help_text='360x220 é a proporção ideal para a imagem', verbose_name='Imagem'),
            preserve_default=True,
        ),
    ]
