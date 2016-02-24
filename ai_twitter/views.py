from django.shortcuts import render
from django.shortcuts import render, render_to_response

from django.template import RequestContext
from .utils import get_n_processed_conversations
from .models import Twitter_Tweet

from django.db.models import Q
from django.db.models import F

# Create your views here.

def demo_conversations_per_page(request, pageno):
    context = RequestContext(request)


    conversation_ids = get_n_processed_conversations(10, int(pageno))

    conversation_contexts = []

    for conversation_id in conversation_ids:
        #conversation = Twitter_Tweet.objects.filter(Q(tweet_id=str(conversation_id)))[0]

        conversation = Twitter_Tweet.objects.filter(Q(tweet_id=conversation_id) & Q(conversation_id=conversation_id))[0]
        tweet_response = Twitter_Tweet.objects.filter(~Q(tweet_id=conversation_id) & Q(conversation_id=conversation_id))[0]
        ai_response = tweet_response.processed_content

        conversation_contexts.append([conversation, tweet_response, ai_response])


    return render_to_response('twitter/demo_conversations_by_page.html', {'conversation_contexts':conversation_contexts}, context_instance=context)

def demo_conversations(request):
    context = RequestContext(request)


    conversation_ids = get_n_processed_conversations()

    conversation_contexts = []

    for conversation_id in conversation_ids:
        #conversation = Twitter_Tweet.objects.filter(Q(tweet_id=str(conversation_id)))[0]

        conversation = Twitter_Tweet.objects.filter(Q(tweet_id=conversation_id) & Q(conversation_id=conversation_id))[0]
        tweet_response = Twitter_Tweet.objects.filter(~Q(tweet_id=conversation_id) & Q(conversation_id=conversation_id))[0]
        ai_response = tweet_response.processed_content

        conversation_contexts.append([conversation, tweet_response, ai_response])


    return render_to_response('twitter/demo_conversations.html', {'conversation_contexts':conversation_contexts}, context_instance=context)

