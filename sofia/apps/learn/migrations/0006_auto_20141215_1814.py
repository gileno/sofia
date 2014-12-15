# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0005_auto_20141215_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='area',
            field=models.ForeignKey(related_name='projects', on_delete=django.db.models.deletion.SET_NULL, blank=True, verbose_name='Área', to='learn.Area', null=True),
            preserve_default=True,
        ),
    ]
