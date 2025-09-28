from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from .models import Genre, Book
from django.views import View
from .forms import Search

@method_decorator(cache_page(60*15), name='dispatch')
class booksview(View):
    def get(self, request, slug=None):
        genre = None
        if slug:
            genre = get_object_or_404(Genre, slug=slug)
            books = Book.objects.filter(genres=genre)
        else:
            books = Book.objects.all()
        return render(request, 'books/books.html', {
            'books': books,
            'genre': genre,
        })

@method_decorator(cache_page(60*15), name='dispatch')
class bookview(View):
    def get(self, request, id):
        book = get_object_or_404(Book, id=id)
        return render(request, 'books/book.html',{
            'book': book,
        })

@method_decorator(cache_page(60*15), name='dispatch')
class searchview(View):
    def get(self, request):
        form = Search(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            query = cd['query']
            books = Book.objects.filter(title__icontains=query)
            return render(request, 'books/books.html',{
                'books': books,
            })