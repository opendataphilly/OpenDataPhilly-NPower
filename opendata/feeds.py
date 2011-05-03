from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from models import Resource, Tag

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
        return "/opendata/resource/%i" % item.id

    def item_description(self, item):
        return item.short_description


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
        return "/opendata/resource/%i" % item.id

    def item_description(self, item):
        return item.short_description

