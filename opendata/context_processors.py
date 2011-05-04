from datetime import datetime
import pytz
from pytz import timezone
from django.conf import settings
from django.core.cache import cache
from models import TwitterCache
import twitter
import simplejson as json

def latest_tweets( request ):
    tweets = cache.get( 'tweets' )

    utc = pytz.utc
    local = timezone('US/Eastern')

    if tweets:
        return {"tweets": tweets}
    
    tweets = twitter.Api().GetUserTimeline( settings.TWITTER_USER )[:4]
    if tweets.count < 4:
        tweet_cache = []
        for t in TwitterCache.objects.all():
            tc = json.JSONDecoder().decode(t.text)
            tc['date'] = datetime.strptime( tc['created_at'], "%a %b %d %H:%M:%S +0000 %Y" ).replace(tzinfo=utc).astimezone(local)
            tweet_cache.append(tc)
        return {'tweets': tweet_cache}
        
    TwitterCache.objects.all().delete()
    for tweet in tweets:
        tweet.date = datetime.strptime( tweet.created_at, "%a %b %d %H:%M:%S +0000 %Y" ).replace(tzinfo=utc).astimezone(local)
        t = TwitterCache(text=tweet.AsJsonString())
        t.save()
    cache.set( 'tweets', tweets, settings.TWITTER_TIMEOUT )
    
    return {"tweets": tweets}

def get_current_path(request):
    return {'current_path': request.get_full_path(), 'current_host': request.get_host()}

def get_settings(request):
    return {'SITE_ROOT': settings.SITE_ROOT}

