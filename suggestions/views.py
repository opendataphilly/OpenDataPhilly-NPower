from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from models import *
from forms import *

def list_all(request):
    suggestions = Suggestion.objects.order_by("-rating_score")
    form = SuggestionForm()
    return render_to_response('suggestions/list.html', {'suggestions': suggestions, 'form': form}, context_instance=RequestContext(request))
    
def add_suggestion(request):
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():

            sug = Suggestion()
            sug.suggested_by = request.user
            sug.text = request.POST.get('text')
            
            sug.save()            
            sug.rating.add(score=1, user=request.user, ip_address=request.META['REMOTE_ADDR'])
            
            return HttpResponseRedirect('../')
    else: 
        form = SuggestionForm()

    suggestions = Suggestion.objects.order_by("rating_score")
    return render_to_response('suggestions/list.html', {'suggestions': suggestions, 'form': form}, context_instance=RequestContext(request))

def add_vote(request, suggestion_id):
    suggestion = Suggestion.objects.get(pk=suggestion_id)
    did_vote = suggestion.rating.get_rating_for_user(request.user, request.META['REMOTE_ADDR'])
    if did_vote == None:
        suggestion.rating.add(score=1, user=request.user, ip_address=request.META['REMOTE_ADDR'])
    return HttpResponseRedirect('../../')
