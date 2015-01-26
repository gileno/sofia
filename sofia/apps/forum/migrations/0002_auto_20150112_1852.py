# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='right_answer',
            field=models.BooleanField(verbose_name='Resposta Correta?', default=False),
            preserve_default=True,
        ),
    ]
