# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

def user(request, user_name):
    print user_name
    response_dictionary = {'hello_world': 'hello world1'}
    return render_to_response('home.html',
                          response_dictionary,
                          context_instance=RequestContext(request))
