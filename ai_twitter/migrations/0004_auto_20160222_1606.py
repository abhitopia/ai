# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ai_twitter', '0003_auto_20160222_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitter_tweet',
            name='is_display',
            field=models.BooleanField(default=False, verbose_name=b'Should it display'),
        ),
    ]
