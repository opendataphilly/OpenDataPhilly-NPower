from opendata.models import *
from django.contrib import admin

class UrlInline(admin.TabularInline):
    model = Url
    extra = 3
    verbose_name = 'Resource Url'
    verbose_name_plural = 'Resource Urls'

class ResourceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':[('name', 'is_published'), 'description','usage', ('organization', 'division'), ('contact_phone', 'contact_email', 'contact_url')]}),
        ('Metadata Fields ', {'fields':['release_date', ('time_period', 'update_frequency'), ('data_formats', 'area_of_interest'), 'proj_coord_sys', ('metadata_user', 'metadata_contact'), 'metadata_notes', 'tags'], 'classes':['collapse', 'wide']})
    ]
    inlines = [UrlInline,]
    list_display = ('name', 'organization', 'release_date', 'is_published')
    search_fields = ['name', 'organization']
    list_filter = ['tags', 'is_published']
    date_heirarchy = 'release_date'



admin.site.register(Tag)
admin.site.register(UrlType)
admin.site.register(Url)
admin.site.register(Resource, ResourceAdmin)