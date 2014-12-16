# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0008_announcement'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='fixed',
            field=models.BooleanField(verbose_name='Anúncio Fixo?', default=False),
            preserve_default=True,
        ),
    ]
