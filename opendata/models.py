from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    tag_name = models.CharField(max_length=150)

    def __unicode__(self):
        return self.tag_name

    class Meta: 
        ordering = ['tag_name']

class DataType(models.Model):
    data_type = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.data_type
        
    class Meta: 
        ordering = ['data_type']

class UrlType(models.Model):
    url_type = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.url_type
    
    class Meta: 
        ordering = ['url_type']
    
class Resource(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    short_description = models.CharField(max_length=255, blank=True)
    usage = models.TextField()
    organization = models.CharField(max_length=255)
    division = models.CharField(max_length=255, blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    contact_email = models.CharField(max_length=255, blank=True)
    contact_url = models.CharField(max_length=255, blank=True)
    
    release_date = models.DateField(blank=True, null=True)
    time_period = models.CharField(max_length=50, blank=True)
    update_frequency = models.CharField(max_length=255, blank=True)
    data_formats = models.CharField(max_length=255, blank=True)
    area_of_interest = models.CharField(max_length=255, blank=True)
    proj_coord_sys = models.CharField(max_length=255, blank=True, verbose_name="Coordinate system")
    is_published = models.BooleanField(default=True, verbose_name="Available to the public")
    
    created_by = models.ForeignKey(User, related_name='created_by')
    last_updated_by = models.ForeignKey(User, related_name='updated_by')
    created = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(auto_now=True)
    metadata_contact = models.CharField(max_length=255, blank=True)
    metadata_notes = models.TextField(blank=True)
    
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    data_types = models.ManyToManyField(DataType, blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
class Url(models.Model):
    url = models.CharField(max_length=255, blank=True)
    url_label = models.CharField(max_length=255, blank=True)
    url_type = models.ForeignKey(UrlType, null=True, blank=True)
    resource = models.ForeignKey(Resource)

    def __unicode__(self):
        return self.url
