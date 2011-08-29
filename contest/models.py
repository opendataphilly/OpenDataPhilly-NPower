from django.db import models
from django.contrib.auth.models import User

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
    nominator = models.CharField(max_length=255)
    nominator_link = models.CharField(max_length=255)
    
    contest = models.ForeignKey(Contest)


    def __str__(self):
        return self.title

    def get_vote_count(self):
        return self.vote_set.objects.count()

class Vote(models.Model):
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now=True)

    entry = models.ForeignKey(Entry)

