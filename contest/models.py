from django.db import models
from djangoratings.fields import RatingField

# Create your models here.

class Contest(models.Model):
    title = models.CharField(max_length=255)    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    rules = models.TextField()

    def __str__(self):
        return self.title

class Entry(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    nominator = models.CharField(max_length=255)
    nominator_link = models.CharField(max_length=255)
    
    contest = models.ForeignKey(Contest)

    rating = RatingField(range=1, allow_delete=True, can_change_vote=True)

    def __str__(self):
        return self.title
