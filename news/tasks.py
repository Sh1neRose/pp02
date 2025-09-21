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
                res = requests.get(entry.link)
                soup = BeautifulSoup(res.text, 'lxml')
                blocks = soup.find_all('div', {'data-component':'text-block'})
                description = []
                for block in blocks:
                    for child in block.children:
                        if child.name == 'p':
                            description.append(child.get_text())
                        elif child.name in ['ul', 'ol']:
                            for li in child.find_all('li'):
                                description.append('- ' + li.get_text())
                News.objects.create(
                    title=entry.title,
                    link=entry.link,
                    category=category,
                    summary=entry.summary,
                    description=description,
                    published_at=make_aware(datetime.fromtimestamp(mktime(entry.published_parsed))),
                )