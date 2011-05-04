from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from models import Resource, Tag, Idea

class ResourcesFeed(Feed):
    title = "OpenDataPhilly.org: Resources"
    link = "/feeds/resources/"
    description = "List of resources on OpenDataPhilly.org listed in the order they were added"
    description_template = "feeds/resource.html"

    def items(self):
        return Resource.objects.order_by('-created')
    def item_title(self, item):
        return item.name
    def item_link(self, item):
        return item.get_absolute_url()
    def item_description(self, item):
        return item.short_description

class IdeasFeed(Feed):
    title = "OpenDataPhilly.org: Ideas"
    link = "/feeds/ideas/"
    description = "List of ideas on OpenDataPhilly.org listed in the order they were added"
    description_template = "feeds/idea.html"

    def items(self):
        return Idea.objects.order_by('-created_by_date')
    def item_title(self, item):
        return item.title
    def item_link(self, item):
        return item.get_absolute_url()
    def item_author_name(self, item):
        return item.author
    def item_description(self, item):
        return item.description

class TagFeed(Feed):
    description_template = "feeds/resource.html"
    
    def get_object(self, request, tag_id):
        return get_object_or_404(Tag, pk=tag_id)
    def title(self, obj):
        return "OpenDataPhilly.org: Resources in %s" % obj.tag_name
    def link(self, obj):
        return "/feeds/tag/%i" % obj.id
    def description(self, obj):
        return "Resources with the tag %s in the order they were added" % obj.tag_name

    def items(self, obj):
        return Resource.objects.filter(tags=obj).order_by('-created')
    def item_title(self, item):
        return item.name
    def item_link(self, item):
        return item.get_absolute_url()

    def item_description(self, item):
        return item.short_description

