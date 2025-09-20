from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from news.models import News

@shared_task
def send_mail_task(emails, new_id):
    new = News.objects.get(id=new_id)
    subject = f'Latest news in the category {new.category}'
    message = f'''
        Latest news
        {new}
        {new.summary}
        {new.get_absolute_url()}
        {new.published_at}
    '''
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        emails,
    )

