from celery import shared_task
from .utils import get_tweets_by_user, get_tweets_mentioning_user

@shared_task(name='ai_twitter.tasks.collect_data_from_twitter')
def collect_data_from_twitter():
    get_tweets_by_user('', '')
    get_tweets_mentioning_user('', '')