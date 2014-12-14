# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='blocked',
            field=models.BooleanField(verbose_name='Bloqueado', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='material',
            name='order',
            field=models.PositiveSmallIntegerField(verbose_name='Ordem', blank=True, default=0, help_text='Ordem crescente da listagem dos materiais'),
            preserve_default=True,
        ),
    ]
