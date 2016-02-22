from celery import shared_task
from .utils import get_tweets_by_user, \
    get_tweets_mentioning_user, \
    get_latest_valid_conversation_id, \
    generate_conversation_context, \
    get_context_generated_conversation, \
    generate_conversation_output

@shared_task(name='ai_twitter.tasks.collect_data_from_twitter')
def collect_data_from_twitter():
    get_tweets_by_user('', '')
    get_tweets_mentioning_user('', '')

@shared_task(name='ai_twitter.tasks.generate_context_output')
def generate_context_output():
    conversation_id = get_latest_valid_conversation_id()

    print '---conversation context----'
    print conversation_id
    if conversation_id != None:
        generate_conversation_context(conversation_id)
        generate_conversation_output(conversation_id)

"""
@shared_task(name='ai_twitter.tasks.generate_output')
def generate_output():
    conversation_id = get_context_generated_conversation()

    print '---conversation output----'
    print conversation_id
    if conversation_id != None:
        generate_conversation_output(conversation_id)
"""