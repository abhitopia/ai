from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render, render_to_response

# Create your views here.
def home(request):
    context = RequestContext(request)
    return render_to_response('core/index.html', context_instance=context)