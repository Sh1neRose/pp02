from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(null=False, blank=False)
    feed_url = models.URLField(null=False, blank=False)

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.TextField(blank=True, null=True)
    link = models.URLField(unique=True, max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news')
    summary = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('news:full_new', args=[self.id])
    