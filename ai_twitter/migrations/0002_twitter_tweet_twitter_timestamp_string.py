# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ai_twitter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitter_tweet',
            name='twitter_timestamp_string',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Tweet timestamp', blank=True),
        ),
    ]
