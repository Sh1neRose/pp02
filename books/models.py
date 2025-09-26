from django.db import models
from django.urls import reverse

class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=False, null=False)
    url = models.URLField(blank=False, null=False)

    def __str__(self):
        return self.name
    
class Author(models.Model):
    goodreads_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    goodreads_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    rating_count = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books', null=True)
    genres = models.ManyToManyField(Genre, related_name='books')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('books:book', kwargs={'id': self.id})

