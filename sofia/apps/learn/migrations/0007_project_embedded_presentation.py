# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0006_auto_20141215_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='embedded_presentation',
            field=models.TextField(blank=True, verbose_name='Apresentação Embarcada (youtube/vimeo)', default='', help_text='html embarcado de uma apresentação, ex: vídeo do youtube'),
            preserve_default=True,
        ),
    ]
