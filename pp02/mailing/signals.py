from django.dispatch import receiver
from django.db.models.signals import post_save
from news.models import News
from .models import Subscriber
from .tasks import send_mail_task

batch_size = 5

@receiver(post_save, sender=News)
def send_mails(sender, instance, created, *args, **kwargs):
    if created:
        emails = list(Subscriber.objects.filter(is_active=True, category=instance.category).values_list('email', flat=True))
        for i in range(0, len(emails), batch_size):
            batch = emails[i:i+batch_size]
            send_mail_task.delay(batch, instance.id)
    