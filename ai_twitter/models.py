from django.db import models

class Twitter_User(models.Model):
    """
    Twitter User model
    """
    screen_name = models.CharField(verbose_name='Twitter handle name', max_length=200, unique=True, blank=True)
    user_name = models.CharField(verbose_name='Twitter user name', max_length=200, null=True, blank=True)
    image_url = models.CharField(verbose_name='Profile image url', max_length=200, null=True, blank=True)

# Create your models here.
class Twitter_Tweet(models.Model):
    """
    Twitter Tweet
    """

    tweet_id = models.CharField(verbose_name='Twitter id', max_length=200, unique=True, blank=True)
    timestamp = models.DateTimeField(verbose_name='Created time', auto_now=True)

    content = models.TextField(verbose_name='Content', blank=True, null=True)
    conversation_id = models.CharField(verbose_name='Conversation id', max_length=200, null=True, blank=True)

    twitter_handle_name = models.CharField(verbose_name='Twitter handle name', max_length=200, null=True, blank=True)
    twitter_timestamp = models.DateTimeField(verbose_name='Tweet timestamp', null=True, blank=True)

    is_processed = models.BooleanField(verbose_name='Is processed', default=False)
    processed_content = models.TextField(verbose_name='Processed Content', blank=True, null=True)

    twitter_user = models.ForeignKey(Twitter_User, blank=True, null=True, on_delete=models.SET_NULL)


