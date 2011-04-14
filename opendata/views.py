from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core import serializers
from django.core.mail import send_mail, EmailMessage
from django.template import RequestContext
from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from models import *
from forms import *

def home(request):
    recent = Resource.objects.order_by("-created")[:3]
    idea = Idea.objects.order_by("-created_by_date")[0]
    return render_to_response('home.html', {'recent': recent, 'idea': idea},  context_instance=RequestContext(request))

def results(request):
    resources = Resource.objects.all()
    return render_to_response('results.html', {'results': resources}, context_instance=RequestContext(request))

def thanks(request):
    return render_to_response('thanks.html', context_instance=RequestContext(request))

def tag_results(request, tag_id):
    tag = Tag.objects.get(pk=tag_id)
    tag_resources = Resource.objects.filter(tags=tag)

    return render_to_response('results.html', {'results': tag_resources, 'tag': tag}, context_instance=RequestContext(request))

def search_results(request):
    search_resources = Resource.objects.all()
    if 'qs' in request.GET:
        qs = request.GET['qs'].replace("+", " ")
        search_resources = search_resources.filter(Q(name__icontains=qs) | Q(description__icontains=qs) | Q(organization__icontains=qs) | Q(division__icontains=qs))
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

def suggest_content(request):
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            #do something
            
            coords, types, formats="", "", ""
            for c in request.POST.getlist("coord_system"):
                coords = coords + " EPSG:" + CoordSystem.objects.get(pk=c).EPSG_code.__str__()
            for t in request.POST.getlist("types"):
                types = types + " " + UrlType.objects.get(pk=t).url_type
            for f in request.POST.getlist("formats"):
                formats = formats + " " + DataType.objects.get(pk=f).data_type
                
            data = {
                "submitter": request.user.username,
                "submit_date": datetime.now(),
                "dataset_name": request.POST.get("dataset_name"),
                "organization": request.POST.get("organization"),
                "copyright_holder": request.POST.get("copyright_holder"),
                "contact_email": request.POST.get("contact_email"),
                "contact_phone": request.POST.get("contact_phone"),
                "url": request.POST.get("url"),
                "time_period": request.POST.get("time_period"),
                "release_date": request.POST.get("release_date"),
                "area_of_interest": request.POST.get("area_of_interest"),
                "update_frequency": request.POST.get("update_frequency"),
                "coord_system": coords,
                "types": types,
                "formats": formats,
                "usage_limitations": request.POST.get("usage_limitations"),
                "collection_process": request.POST.get("collection_process"),
                "data_purpose": request.POST.get("data_purpose"),
                "intended_audience": request.POST.get("intended_audience"),
                "why": request.POST.get("why"),
            }
            
            
            subject, from_email, to_email = 'OpenDataPhilly - Data Submission', request.user.email, settings.CONTACT_EMAILS
            text_content = render_to_string('submit_email.txt', data)
            msg = EmailMessage(subject, text_content, from_email, to_email)
            msg.send()
            
            sug_object = Suggestion()
            sug_object.user = request.user
            sug_object.email_text = text_content
            
            sug_object.save()
            
            return HTTPResponseRedirect('/thanks/')
    else: 
        form = SuggestionForm()
        
    return render_to_response('submit.html', {'form': form}, context_instance=RequestContext(request))


## views called by js ajax for object lists
def get_tag_list(request):
    tags = Tag.objects.all()
    return HttpResponse(serializers.serialize("json", tags)) 