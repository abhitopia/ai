__author__ = 'omkar'

import twitter
import time
import csv
import codecs
import os
import random

from .models import Twitter_User
from .models import Twitter_Tweet
from django.db.models import Q
from django.db.models import F
from django.conf import settings

CONSUMER_KEY = "pOLfFTs3OrpGSw7HWWrjxsrwd"
CONSUMER_SECRET = "oSNRjRkcd3GHYVZJWSFzrBcTkpYInprSBsFdTKtkgt03pPcU1M"

ACCESS_TOKEN = "140664325-RNFBAUg55odvMErbErZECo3ejsuOwtZk8xAFEffq"
ACCESS_TOKEN_SECRET = "ADoAjrB6tujLp7Cxmje67BaMrJaYRuhLR0Ay3E6BDyQWY"


REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL = 'https://api.twitter.com/oauth/authenticate'

COMPANIES = [
    'BTCare',
    'greateranglia',
    'LondonMidland',
    'nationalrailenq',
    'northernrailorg',
    'Se_Railway',
    'SpotifyCares',
    'VirginTrains',
    'virginmedia'
]

def create_tweet(result):
    """ Creates a tweet from twitter result json """

    # Iterate through each result
    # Check if the tweet is aldready present
    # If not then store it in database

    tweet_id = str(result.id)
    text = result.text
    conversation_id = str(result.in_reply_to_status_id)

    twitter_handle_name = result.user.screen_name
    profile_image_url = result.user.profile_background_image_url

    user_name = result.user.name

    created_at = result.created_at

    # Check if the tweet user exists in database, if not create.
    try:
        twitter_user = Twitter_User.objects.get(screen_name=twitter_handle_name)
        twitter_user.image_url = profile_image_url
        twitter_user.save()
    except:
        twitter_user = Twitter_User()
        twitter_user.screen_name = twitter_handle_name
        twitter_user.image_url = profile_image_url
        twitter_user.user_name = user_name

        twitter_user.save()


    try:
        tweet = Twitter_Tweet.objects.get(tweet_id=tweet_id)
        tweet.conversation_id = conversation_id

        if conversation_id is None or conversation_id=='None':
            tweet.conversation_id = tweet_id

        tweet.twitter_timestamp_string = str(created_at)
        tweet.save()
    except:
        tweet = Twitter_Tweet()
        tweet.twitter_user = twitter_user
        tweet.content = text

        tweet.conversation_id = conversation_id

        if conversation_id is None or conversation_id=='None':
            tweet.conversation_id = tweet_id

        tweet.tweet_id = tweet_id
        tweet.twitter_handle_name = twitter_handle_name

        tweet.twitter_timestamp_string = str(created_at)

        tweet.save()






def get_tweets_by_user(tweet_user, from_date):
    """ Get the tweets from the user since a particular data.
    """

    api = twitter.Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token_key=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)


    companies_query =  "%20OR%20".join(['from%3A' + company_name for company_name in COMPANIES])

    results = api.GetSearch(raw_query="q="+ companies_query + "%20since%3A2016-02-19&src=typd&count=100")

    i = 0
    for result in results:
        i = i+1
        create_tweet(result)


def get_tweets_mentioning_user(tweet_user, from_date):
    """ Get the tweets from the user since a particular data.
    """

    api = twitter.Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token_key=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)



    companies_query =  "%20OR%20".join(['%40' + company_name for company_name in COMPANIES])

    results = api.GetSearch(raw_query="q=" + companies_query + "%20since%3A2016-02-18&src=typd&count=100")

    i = 0
    for result in results:
        i = i+1

        create_tweet(result)




def get_unprocessed_conversations():
    tweets = Twitter_Tweet.objects.filter(Q(tweet_id=F('conversation_id')) & ~Q(twitter_handle_name__in=COMPANIES))

    return tweets


def get_valid_unprocessed_conversation_ids():
    """ Get all the valid conversation ids
    :return:
    """
    valid_conversation_ids = []

    conversations = get_unprocessed_conversations()
    for conversation in conversations:
        tweets = Twitter_Tweet.objects.filter(Q(conversation_id=conversation.tweet_id)).order_by('tweet_id')
        last_tweet = None

        for tweet in tweets:
            last_tweet = tweet

        # If the last tweet is by BTCare then its a valid query
        if last_tweet.twitter_handle_name in COMPANIES and last_tweet.is_processed is False:
            valid_conversation_ids.append(last_tweet.conversation_id)

    return valid_conversation_ids


def get_latest_valid_conversation_id():
    """ Get the latest conversation id
    :return:
    """

    valid_conversation_ids = get_valid_unprocessed_conversation_ids()

    if len(valid_conversation_ids) > 0:
        return valid_conversation_ids[0]
    else:
        return None


def generate_conversation_context(conversation_id):
    """ Generate the conversation context file.
    :param conversation_id:
    :return:
    """
    tweets = Twitter_Tweet.objects.filter(Q(conversation_id=conversation_id)).order_by('tweet_id')


    try:
        with open(settings.BASE_DIR + '/csv/context-' + conversation_id, 'wb') as csvfile:
            for tweet in tweets:

                context_writer = csv.writer(csvfile)
                context_writer.writerow([tweet.tweet_id, tweet.conversation_id, tweet.twitter_timestamp, tweet.twitter_handle_name, tweet.twitter_user.user_name, "", unicode(tweet.content).encode("utf-8")])

        # Update the tweets with that conversation id as context generated.
        Twitter_Tweet.objects.filter(Q(conversation_id=conversation_id)).update(is_context_generated=True)
    except:
        print 'file write error'





def get_context_generated_conversation():
    """  Get the conversation for which the context has been generated, but output has not been generated.
    :param conversation_id:
    :return:
    """

    # Query for the conversations for which context generated is true and output has not been generated
    conversations = Twitter_Tweet.objects.filter(Q(tweet_id=F('conversation_id')) & Q(is_context_generated=True) & Q(is_processed=True)).order_by('tweet_id')


    if len(conversations) > 0:
        return conversations[0].conversation_id
    else:
        return None



def generate_conversation_output(conversation_id):
    """ Generate the output file from the context file given a conversation.

    :param conversation_id:
    :return:
    """

    RANDOM_LINES = ['SORRY FOR THE INCONVIENIENCE', 'HOW CAN I HELP YOU']

    lines = []

    # Read all the lines.
    with open(settings.BASE_DIR + '/csv/context-' + conversation_id, 'rb') as csvfile:
        """ Replace the last line with the random response """

        context_reader = csv.reader(csvfile)


        for row in context_reader:
            lines.append(row)



    no_of_lines = len(lines)

    # Get the last line.
    lastline = []
    if no_of_lines > 0:
        lastline = lines[no_of_lines - 1]

    generated_response = ''

    # Now put every line into the output file, except for the last line.
    with open(settings.BASE_DIR + '/output/output-' + conversation_id, 'wb') as csvfile:
        context_writer = csv.writer(csvfile)

        """
        for i in xrange(0, no_of_lines - 1):
            line = lines[i]
            context_writer.writerow(line)

        generated_response = RANDOM_LINES[random.randint(0, 1)]
        lastline[len(lastline) - 1] = generated_response
        """
        generated_response = RANDOM_LINES[random.randint(0, 1)]
        context_writer.writerow([generated_response])

    # Update in database for that conversation that context has been generated and is processed is true.
    Twitter_Tweet.objects.filter(Q(tweet_id=lastline[0])).update(
        is_dummy=True,
        is_display=True,
        is_processed=True,
        is_context_generated=True,
        processed_content=generated_response
    )

    Twitter_Tweet.objects.filter(Q(conversation_id=conversation_id)).update(
        is_dummy=True,
        is_display=True,
        is_processed=True,
        is_context_generated=True,
    )





