from django.contrib import admin
from .models import Book, Genre, Author

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'goodreads_id']

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'goodreads_id']
