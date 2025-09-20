from django.db import models
from news.models import Category

class Subscriber(models.Model):
    email = models.EmailField(
        max_length=66,
        )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subscriber'
        )
    is_active = models.BooleanField(
        default=True
        )
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email', 'category'], name='unique_subscriber'),
        ]
