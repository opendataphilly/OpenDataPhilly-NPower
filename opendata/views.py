from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core import serializers
from django.db.models import Q

from models import *

def home(request):
    return render_to_response('home.html')

def results(request):
    return render_to_response('results.html')


def tag_results(request, tag_id):
    tag = Tag.objects.get(pk=tag_id)
    tag_resources = Resource.objects.filter(tags=tag)

    return render_to_response('results.html', {'results': tag_resources, 'tag': tag})

def search_results(request):
    search_resources = Resource.objects.all()
    if 'qs' in request.GET:
        qs = request.GET['qs']
        search_resources = search_resources.filter(Q(name__icontains=qs) | Q(description__icontains=qs))
 
    return render_to_response('results.html', {'results': search_resources})

def resource_details(request, resource_id):
    resource = Resource.objects.get(pk=resource_id)
    return render_to_response('details.html', {'resource': resource}) 
    
    



## views called by js ajax for object lists
def get_tag_list(request):
    tags = Tag.objects.all()
    return HttpResponse(serializers.serialize("json", tags)) 