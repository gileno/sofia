# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0004_auto_20141215_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', blank=True, to='taggit.Tag', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', blank=True, to='taggit.Tag', verbose_name='Tags'),
            preserve_default=True,
        ),
    ]
