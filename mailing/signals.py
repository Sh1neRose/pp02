from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Subscriber
from .tasks import send_book_mail
from books.models import Book

batch_size = 5

@receiver(post_save, sender=Book)
def send_mails(sender, instance, created, *args, **kwargs):
    if created:
        emails = list(Subscriber.objects.filter(is_active=True).values_list('email', flat=True))
        for i in range(0, len(emails), batch_size):
            batch = emails[i:i+batch_size]
            send_book_mail.delay(batch, instance.id)
    