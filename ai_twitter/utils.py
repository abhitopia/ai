__author__ = 'omkar'

import twitter
import time
import csv
import codecs
import os

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
    'GWRHelp',
    'ID_Mobile_UK',
    'LondonMidland',
    'TPOuk',
    'virginmedia',
    'VirginTrains',
    'XboxSupport'
]



#from%3Avirginmedia%20OR%20from%3ABTCare
#%40BTCare%20OR%20%40virginmedia

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
            print 'in if'
            print tweet_id
        else:
            print 'not if'
            print conversation_id


        tweet.twitter_timestamp_string = str(created_at)
        tweet.save()


        print tweet.conversation_id
    except:
        tweet = Twitter_Tweet()
        tweet.twitter_user = twitter_user
        tweet.content = text

        print '-----conversation id------'
        print conversation_id

        tweet.conversation_id = conversation_id

        print type(conversation_id)
        if conversation_id is None or conversation_id=='None':
            tweet.conversation_id = tweet_id
            print 'in if'
            print tweet_id
        else:
            print 'not if'
            print conversation_id


        tweet.tweet_id = tweet_id
        tweet.twitter_handle_name = twitter_handle_name

        tweet.twitter_timestamp_string = str(created_at)

        tweet.save()






def get_tweets_by_user(tweet_user, from_date):
    """
    Get the tweets from the user since a particular data.
    """

    api = twitter.Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token_key=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

    print api.VerifyCredentials()

    companies_query =  "%20OR%20".join(['from%3A' + company_name for company_name in COMPANIES])

    results = api.GetSearch(raw_query="q="+ companies_query + "%20since%3A2016-02-19&src=typd&count=100")

    i = 0
    for result in results:
        i = i+1
        print i
        create_tweet(result)


def get_tweets_mentioning_user(tweet_user, from_date):
    """
    Get the tweets from the user since a particular data.
    """

    api = twitter.Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token_key=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

    print api.VerifyCredentials()

    companies_query =  "%20OR%20".join(['%40' + company_name for company_name in COMPANIES])

    results = api.GetSearch(raw_query="q=" + companies_query + "%20since%3A2016-02-18&src=typd&count=100")

    i = 0
    for result in results:
        i = i+1
        print i
        create_tweet(result)




def get_unprocessed_conversations():
    tweets = Twitter_Tweet.objects.filter(Q(is_processed=False) & Q(tweet_id=F('conversation_id')) & ~Q(twitter_handle_name__in=COMPANIES))

    for tweet in tweets:
        print '-----------'
        print tweet.tweet_id
        print tweet.conversation_id

    return tweets


def get_valid_conversation_ids():
    """
    Get all the valid conversation ids
    :return:
    """
    valid_convesation_ids = []

    conversations = get_unprocessed_conversations()
    for conversation in conversations:
        tweets = Twitter_Tweet.objects.filter(Q(conversation_id=conversation.tweet_id)).order_by('tweet_id')
        last_tweet = None

        for tweet in tweets:
            last_tweet = tweet

        # If the last tweet is by BTCare then its a valid query
        if last_tweet.twitter_handle_name in COMPANIES:
            valid_convesation_ids.append(last_tweet.conversation_id)
            write_conversation_context(last_tweet.conversation_id)

    return valid_convesation_ids

def get_latest_valid_conversation_id():
    """
    Get the latest conversation id
    :return:
    """

    valid_conversation_ids = get_valid_conversation_ids()

    if len(valid_conversation_ids) > 0:
        return valid_conversation_ids[len(valid_conversation_ids) -1]
    else:
        return None

def write_conversation_context(conversation_id):
    tweets = Twitter_Tweet.objects.filter(Q(conversation_id=conversation_id)).order_by('tweet_id')


    with open(settings.BASE_DIR + '/csv/context-' + conversation_id, 'wb') as csvfile:
        for tweet in tweets:

            context_writer = csv.writer(csvfile)
            try:
                context_writer.writerow([tweet.tweet_id, tweet.conversation_id, tweet.twitter_timestamp, tweet.twitter_handle_name, tweet.twitter_user.user_name, "", unicode(tweet.content.strip(codecs.BOM_UTF8)).encode("utf-8")])
            except:
                print 'unicode error'

