# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('forum', '0003_auto_20150112_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, to='taggit.Tag', verbose_name='Tags', through='taggit.TaggedItem', help_text='A comma-separated list of tags.'),
            preserve_default=True,
        ),
    ]
