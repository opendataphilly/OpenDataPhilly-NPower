from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core import serializers
from django.template import RequestContext
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from models import *

def home(request):
    return render_to_response('home.html', context_instance=RequestContext(request))

def results(request):
    resources = Resource.objects.all()
    return render_to_response('results.html', {'results': resources}, context_instance=RequestContext(request))


def tag_results(request, tag_id):
    tag = Tag.objects.get(pk=tag_id)
    tag_resources = Resource.objects.filter(tags=tag)

    return render_to_response('results.html', {'results': tag_resources, 'tag': tag}, context_instance=RequestContext(request))

def search_results(request):
    search_resources = Resource.objects.all()
    if 'qs' in request.GET:
        qs = request.GET['qs']
        search_resources = search_resources.filter(Q(name__icontains=qs) | Q(description__icontains=qs))
    if 'filter' in request.GET:
        f = request.GET['filter']
        search_resources = search_resources.filter(url__url_type__url_type__iexact=f).distinct()
    
    return render_to_response('results.html', {'results': search_resources}, context_instance=RequestContext(request))

def resource_details(request, resource_id):
    resource = Resource.objects.get(pk=resource_id)
    return render_to_response('details.html', {'resource': resource}, context_instance=RequestContext(request)) 
    

def idea_results(request, idea_id=None):
    if idea_id:
        idea = Idea.objects.get(pk=idea_id)
        return render_to_response('idea_details.html', {'idea': idea}, context_instance=RequestContext(request)) 
    
    ideas = Idea.objects.order_by("-created_by_date")
    return render_to_response('ideas.html', {'ideas': ideas}, context_instance=RequestContext(request)) 


## views called by js ajax for object lists
def get_tag_list(request):
    tags = Tag.objects.all()
    return HttpResponse(serializers.serialize("json", tags)) 