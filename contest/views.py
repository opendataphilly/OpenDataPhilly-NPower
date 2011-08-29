from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from contest.models import *

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

    do_vote, next_vote_date = entry.user_can_vote(user)

    if do_vote:
        new_vote = Vote(user=user, entry=entry)
        new_vote.save()
        messages.success(request, 'Your vote has been recorded. You may vote again on ' + next_vote_date.strftime('%A, %b %d %Y'))
    else:
        messages.error(request, 'You have already voted for ' + entry.title + '. You may vote for this entry again on ' + next_vote_date.strftime('%A, %b %d %Y'))    

    return render_to_response('contest/entries.html', {'contest': entry.contest}, context_instance=RequestContext(request))
