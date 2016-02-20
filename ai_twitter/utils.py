__author__ = 'omkar'

import twitter
import time

from .models import Twitter_User
from .models import Twitter_Tweet

CONSUMER_KEY = "pOLfFTs3OrpGSw7HWWrjxsrwd"
CONSUMER_SECRET = "oSNRjRkcd3GHYVZJWSFzrBcTkpYInprSBsFdTKtkgt03pPcU1M"

ACCESS_TOKEN = "140664325-RNFBAUg55odvMErbErZECo3ejsuOwtZk8xAFEffq"
ACCESS_TOKEN_SECRET = "ADoAjrB6tujLp7Cxmje67BaMrJaYRuhLR0Ay3E6BDyQWY"


REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL = 'https://api.twitter.com/oauth/authenticate'


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

        print '-----conversation id------'
        print conversation_id

        print type(conversation_id)
        if conversation_id is None or conversation_id=='None':
            tweet.conversation_id = tweet_id
            print 'in if'
            print tweet_id
        else:
            print 'not if'
            print conversation_id


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


        print tweet.conversation_id

        tweet.tweet_id = tweet_id
        tweet.twitter_handle_name = twitter_handle_name

        tweet.save()






def get_tweets_by_user(tweet_user, from_date):
    """
    Get the tweets from the user since a particular data.
    """

    api = twitter.Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token_key=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

    print api.VerifyCredentials()

    results = api.GetSearch(raw_query="q=from%3ABTCare%20since%3A2016-02-19&src=typd&count=100")

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

    results = api.GetSearch(raw_query="q=%40BTCare%20since%3A2016-02-18&src=typd&count=100")

    i = 0
    for result in results:
        i = i+1
        print i
        create_tweet(result)


