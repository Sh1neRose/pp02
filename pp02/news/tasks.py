from celery import shared_task
import feedparser
from .models import News
from django.utils.timezone import make_aware
from datetime import datetime
from time import mktime

@shared_task
def update_news():
    bbc = feedparser.parse('https://feeds.bbci.co.uk/news/rss.xml')
    entries = bbc.entries

    for entry in entries:
        if not News.objects.filter(link=entry.link).exists():
            News.objects.create(
                title=entry.title,
                link=entry.link,
                summary=entry.summary,
                published_at=make_aware(datetime.fromtimestamp(mktime(entry.published_parsed))),
            )