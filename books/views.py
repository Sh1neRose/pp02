from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from .models import Genre, Book
from django.views import View

class booksview(View):
    def get(self, request, slug=None):
        genre = None
        if slug:
            genre = get_object_or_404(Genre, slug=slug)
            books = Book.objects.filter(genre=genre)
        else:
            books = Book.objects.all()
        return render(request, 'books/books.html', {
            'books': books,
            'genre': genre,
        })
    
class bookview(View):
    def get(self, request, id):
        book = get_object_or_404(Book, id=id)
        return render(request, 'books/book.html',{
            'book': book,
        })