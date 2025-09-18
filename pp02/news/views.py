from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import News, Category

class news(View):
    def get(self, request, slug=None, *args, **kwargs):
        category = None
        if slug:
            category = get_object_or_404(Category, slug=slug)
            news = News.objects.filter(category=category)
        else:
            news = News.objects.all()
        return render(request, 'news/main.html', {
            'news': news,
            'category': category,
        })
    
class full_new(View):
    def get(self, request, id):
        new = get_object_or_404(News, id=id)
        return render(request,'news/full_new.html',{
            'new': new,
        })