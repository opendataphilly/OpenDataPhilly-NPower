from datetime import datetime
from opendata.models import *
from django.contrib import admin

class UrlInline(admin.TabularInline):
    model = Url
    extra = 0
    verbose_name = 'Resource Url'
    verbose_name_plural = 'Resource Urls'

class ResourceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':[('name', 'is_published'), 'description', 'short_description', 'usage', 
            ('organization', 'division'), ('contact_phone', 'contact_email', 'contact_url')]}),
        ('Metadata Fields ', {'fields':['release_date', ('time_period', 'update_frequency'), 
            ('data_formats', 'area_of_interest'), 'proj_coord_sys', 'metadata_contact',
            ('created_by', 'created'),
            ('last_updated_by', 'last_updated'),
            'metadata_notes', 'tags', 'data_types'], 'classes':['wide']})
    ]
    readonly_fields = ['created_by', 'created', 'last_updated_by', 'last_updated']
    inlines = [UrlInline,]
    
    list_display = ('name', 'organization', 'release_date', 'is_published')
    search_fields = ['name', 'organization']
    list_filter = ['tags', 'is_published']
    date_heirarchy = 'release_date'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.created = datetime.now()
        
        obj.last_updated_by = request.user
        obj.save()


admin.site.register(DataType)
admin.site.register(Tag)
admin.site.register(UrlType)
admin.site.register(Url)
admin.site.register(Resource, ResourceAdmin)