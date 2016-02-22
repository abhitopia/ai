# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ai_twitter', '0002_twitter_tweet_twitter_timestamp_string'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitter_tweet',
            name='is_context_generated',
            field=models.BooleanField(default=False, verbose_name=b'Is context generated for this conversation'),
        ),
        migrations.AddField(
            model_name='twitter_tweet',
            name='is_display',
            field=models.BooleanField(default=True, verbose_name=b'Should it display'),
        ),
        migrations.AddField(
            model_name='twitter_tweet',
            name='is_dummy',
            field=models.BooleanField(default=False, verbose_name=b'Is it dummy'),
        ),
    ]
