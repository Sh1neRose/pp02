from django.shortcuts import render
from django.views import View
from .models import News

class news(View):
    def get(self, request, *args, **kwargs):
        news = News.objects.all()
        return render(request, 'news/main.html', {
            'news': news,
        })
    