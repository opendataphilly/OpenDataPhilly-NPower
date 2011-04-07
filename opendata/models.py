import os

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from sorl.thumbnail.fields import ImageWithThumbnailsField
from djangoratings.fields import RatingField


class Tag(models.Model):
    tag_name = models.CharField(max_length=150)

    def __unicode__(self):
        return '%s' % self.tag_name

    class Meta: 
        ordering = ['tag_name']

class DataType(models.Model):
    data_type = models.CharField(max_length=50)
    
    def __unicode__(self):
        return '%s' % self.data_type
        
    class Meta: 
        ordering = ['data_type']

class UrlType(models.Model):
    url_type = models.CharField(max_length=50)
    
    def __unicode__(self):
        return '%s' % self.url_type
    
    class Meta: 
        ordering = ['url_type']

class UpdateFrequency(models.Model):
    update_frequency = models.CharField(max_length=50)
    
    def __unicode__(self):
        return '%s' % self.update_frequency
    
    class Meta: 
        ordering = ['update_frequency']

class CoordSystem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    EPSG_code = models.IntegerField(blank=True, help_text="Official EPSG code, numbers only")
    
    def __unicode__(self):
        return '%s, %s' % (self.EPSG_code, self.name)
        
    class Meta: 
        ordering = ['EPSG_code']
        verbose_name = 'Coordinate system'
    
class Resource(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    short_description = models.CharField(max_length=255)
    usage = models.TextField()
    organization = models.CharField(max_length=255)
    division = models.CharField(max_length=255, blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    contact_email = models.CharField(max_length=255, blank=True)
    contact_url = models.CharField(max_length=255, blank=True)
    
    release_date = models.DateField(blank=True, null=True)
    time_period = models.CharField(max_length=50, blank=True)
    update_frequency = models.CharField(max_length=255, blank=True)
    updates = models.ForeignKey(UpdateFrequency, null=True, blank=True)
    data_formats = models.CharField(max_length=255, blank=True)
    area_of_interest = models.CharField(max_length=255, blank=True)
    proj_coord_sys = models.CharField(max_length=255, blank=True, verbose_name="Coordinate system")
    is_published = models.BooleanField(default=True, verbose_name="Public")
    
    created_by = models.ForeignKey(User, related_name='created_by')
    last_updated_by = models.ForeignKey(User, related_name='updated_by')
    created = models.DateTimeField()
    last_updated = models.DateTimeField(auto_now=True)
    metadata_contact = models.CharField(max_length=255, blank=True)
    metadata_notes = models.TextField(blank=True)
    
    coord_sys = models.ManyToManyField(CoordSystem, blank=True, null=True, verbose_name="Coordinate system")
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    data_types = models.ManyToManyField(DataType, blank=True, null=True)
    
    rating = RatingField(range=5, can_change_vote=True)
    
    def get_distinct_url_types(self):
        types = []
        for url in self.url_set.all():
            if url.url_type not in types:
                types.append(url.url_type)
        return types
    
    def get_grouped_urls(self):
        urls = {}
        for utype in UrlType.objects.all():            
            urls[utype.url_type] = self.url_set.filter(url_type=utype)            
        return urls
    
    def get_first_image(self):
        images = UrlImage.objects.filter(url__resource=self)
        if images.count() == 0:
            return None
        return images[0]
    
    def get_images(self):
        images = UrlImage.objects.filter(url__resource=self)
        if images.count() == 0:
            return None
        return images
    
    def __unicode__(self):
        return '%s' % self.name
    
class Url(models.Model):
    url = models.CharField(max_length=255, blank=True)
    url_label = models.CharField(max_length=255, blank=True)
    url_type = models.ForeignKey(UrlType, null=True, blank=True)
    resource = models.ForeignKey(Resource)

    def __unicode__(self):
        return '%s - %s - %s' % (self.url_label, self.url_type, self.url)

class UrlImage(models.Model):
    def get_image_path(instance, filename):
        fsplit = filename.split('.')
        extra = 1
        test_path = os.path.join(settings.MEDIA_ROOT, 'url_images', str(instance.url_id), fsplit[0] + '_' + str(extra) + '.' + fsplit[1])
        while os.path.exists(test_path):
           extra += 1
           test_path = os.path.join(settings.MEDIA_ROOT, 'url_images', str(instance.url_id), fsplit[0] + '_' + str(extra) + '.' +  fsplit[1])
        path = os.path.join('url_images', str(instance.url_id), fsplit[0] + '_' + str(extra) + '.' + fsplit[1])
        return path
        
    url = models.ForeignKey(Url)
    image = ImageWithThumbnailsField(upload_to=get_image_path, thumbnail={'size': (80, 80)}, help_text="The site will resize this master image as necessary for page display")
    title = models.CharField(max_length=255, help_text="For image alt tags")
    source = models.CharField(max_length=255, help_text="Source location or person who created the image")
    source_url = models.CharField(max_length=255, blank=True)
    
    def __unicode__(self):
        return '%s' % (self.image)
        
