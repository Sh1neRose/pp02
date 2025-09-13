from celery import shared_task
import feedparser
from .models import News, Category
from django.utils.timezone import make_aware
from datetime import datetime
from time import mktime
from bs4 import BeautifulSoup
import requests


@shared_task(bind=True)
def update_news(self):
    categories = Category.objects.all()
    for category in categories:
        bbc = feedparser.parse(category.feed_url)
        entries = bbc.entries
        for entry in entries:
            if not News.objects.filter(link=entry.link).exists():
                News.objects.create(
                    title=entry.title,
                    link=entry.link,
                    category=category,
                    summary=entry.summary,
                    published_at=make_aware(datetime.fromtimestamp(mktime(entry.published_parsed))),
                )