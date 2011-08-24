from django.shortcuts import render_to_response
from django.template import RequestContext
from contest.models import *

def get_entries(request, contest_id):
    contest = Contest.objects.get(pk=contest_id)
    return render_to_response('contest/entries.html', {'contest': contest}, context_instance=RequestContext(request))

def get_rules(request, contest_id):
    contest = Contest.objects.get(pk=contest_id)
    return render_to_response('contest/rules.html', {'contest': contest}, context_instance=RequestContext(request))
