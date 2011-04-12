from datetime import datetime
from django.conf import settings
from django.core.cache import cache
import twitter

def latest_tweets( request ):
    tweets = cache.get( 'tweets' )

    if tweets:
        return {"tweets": tweets}

    tweets = twitter.Api().GetUserTimeline( settings.TWITTER_USER )[:7]
    for tweet in tweets:
        tweet.date = datetime.strptime( tweet.created_at, "%a %b %d %H:%M:%S +0000 %Y" )
    cache.set( 'tweets', tweets, settings.TWITTER_TIMEOUT )

    return {"tweets": tweets}
