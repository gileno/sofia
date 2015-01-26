# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20150112_1852'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='name',
            new_name='title',
        ),
    ]
