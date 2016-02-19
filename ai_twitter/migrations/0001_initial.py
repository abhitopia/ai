# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Twitter_Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tweet_id', models.CharField(unique=True, max_length=200, verbose_name=b'Twitter id', blank=True)),
                ('timestamp', models.DateTimeField(auto_now=True, verbose_name=b'Created time')),
                ('content', models.TextField(null=True, verbose_name=b'Content', blank=True)),
                ('conversation_id', models.CharField(max_length=200, null=True, verbose_name=b'Conversation id', blank=True)),
                ('twitter_handle_name', models.CharField(max_length=200, null=True, verbose_name=b'Twitter handle name', blank=True)),
                ('twitter_timestamp', models.DateTimeField(null=True, verbose_name=b'Tweet timestamp', blank=True)),
                ('is_processed', models.BooleanField(default=False, verbose_name=b'Is processed')),
                ('processed_content', models.TextField(null=True, verbose_name=b'Processed Content', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Twitter_User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('screen_name', models.CharField(unique=True, max_length=200, verbose_name=b'Twitter handle name', blank=True)),
                ('user_name', models.CharField(max_length=200, null=True, verbose_name=b'Twitter user name', blank=True)),
                ('image_url', models.CharField(max_length=200, null=True, verbose_name=b'Profile image url', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='twitter_tweet',
            name='twitter_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='ai_twitter.Twitter_User', null=True),
        ),
    ]
