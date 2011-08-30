from django.db import models
from django.contrib.auth.models import User

import datetime
from datetime import datetime as dt

# Create your models here.

class Contest(models.Model):
    title = models.CharField(max_length=255)    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    vote_frequency = models.IntegerField()
    rules = models.TextField()

    def __str__(self):
        return self.title

class Entry(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    short_description = models.CharField(max_length=120)
    nominator = models.CharField(max_length=255)
    nominator_link = models.CharField(max_length=255)
    
    contest = models.ForeignKey(Contest)


    def __str__(self):
        return self.title

    def get_vote_count(self):
        return self.vote_set.count()

    def get_next_vote_date(self, user):
        votes = self.vote_set.filter(user=user).order_by('timestamp')
        increment = datetime.timedelta(days=self.contest.vote_frequency)
        last_vote_date = votes[0].timestamp
        next_vote_date = last_vote_date + increment 
        return next_vote_date

    def user_can_vote(self, user):
        votes = self.vote_set.filter(user=user).order_by('timestamp')
        next_date = self.get_next_vote_date(user)
        if votes:           
            if dt.today() < next_date and dt.today() < self.contest.end_date:
                return False
        return True

class Vote(models.Model):
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now=True)

    entry = models.ForeignKey(Entry)


from django import forms

class EntryForm(forms.Form):
    org_name = forms.CharField(max_length=255, label="Organization Name")
    org_url = forms.CharField(max_length=255, label="Organization Url")
    contact_person = forms.CharField(max_length=150, label="Contact Person")
    contact_phone = forms.CharField(max_length=15, label="Contact Phone Number")
    contact_email = forms.EmailField(max_length=150, label="Contact Email")
    data_set = forms.CharField(max_length=255, label="Data Set to Nominate")
    data_use = forms.CharField(max_length=1000, widget=forms.Textarea, label="If this data set were available, how would your organization use it?")
    data_mission = forms.CharField(max_length=1000, widget=forms.Textarea, label="How would this data set contribute to your organization's mission")
    

