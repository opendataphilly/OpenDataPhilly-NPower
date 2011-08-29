from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from contest.models import *

import datetime
from datetime import datetime as dt

def get_entries(request, contest_id):
    contest = Contest.objects.get(pk=contest_id)
    return render_to_response('contest/entries.html', {'contest': contest}, context_instance=RequestContext(request))

def get_rules(request, contest_id):
    contest = Contest.objects.get(pk=contest_id)
    return render_to_response('contest/rules.html', {'contest': contest}, context_instance=RequestContext(request))

def get_entry(request, entry_id):
    entry = Entry.objects.get(pk=entry_id)
    return render_to_response('contest/entry.html', {'entry': entry}, context_instance=RequestContext(request))

@login_required
def add_vote(request, entry_id):
    entry = Entry.objects.get(pk=entry_id)
    user = User.objects.get(username=request.user)
    votes = entry.vote_set.objects.filter(user=user).order_by(timestamp)

    if votes:
        last_vote_date = votes[0].timestamp
        increment = datetime.timedelta(days=entry.contest.vote_frequency)
        next_vote_date = last_vote_date + increment 
        if dt.today() < next_vote_date and dt.today() < entry.contest.end_date:
            return render_to_response('contest/entries.html', {'contest': contest}, context_instance=RequestContext(request))

    new_vote = Vote(user=user, entry=entry)
    new_vote.save()
    
    return render_to_response('contest/entries.html', {'contest': contest}, context_instance=RequestContext(request))
