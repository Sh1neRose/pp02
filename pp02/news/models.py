from django.db import models

class News(models.Model):
    title = models.TextField(blank=True, null=True)
    link = models.URLField(unique=True, max_length=500)
    summary = models.TextField(blank=True, null=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title