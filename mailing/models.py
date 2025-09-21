from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(
        max_length=66,
        unique=True,
        )
    is_active = models.BooleanField(
        default=False,
        )
    
    def __str__(self):
        return self.email