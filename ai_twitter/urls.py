from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^demo_conversations/', views.demo_conversations, name='demo_conversations'),
    url(r'^demo_conversations_per_page/(?P<pageno>[\d-]*)', views.demo_conversations_per_page),
]