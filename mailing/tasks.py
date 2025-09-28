from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from books.models import Book
from django.urls import reverse

@shared_task(queue='mailing')
def send_book_mail(emails, new_id):
    book = Book.objects.get(id=new_id)
    book_url = f'{settings.SITE_URL}{book.get_absolute_url()}'
    unsubscribe_url = f'{settings.SITE_URL}{reverse('mailing:unsubscribe')}'
    subject = f'Latest book'
    message = f'''
        Latest book
        {book}
        {book.author}
        {book_url}

        If you want unsubscribe click the link below:
        {unsubscribe_url}
    '''
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        emails,
        fail_silently=False,
    )

@shared_task(queue='mailing')
def confirm_subscribe_mail(email):
    from django.core import signing
    token = signing.dumps({'email': email})
    confirm_url = f'{settings.SITE_URL}{reverse('mailing:subscribe_confirm', kwargs={'token': token,})}'
    subject = 'Confirm Email'
    message = f'''
    Hello {email},

    Please click the link below to confirm your email to receive the latest news:
    {confirm_url}
    '''

    html_message = f'''
    <h2>Please click the link below to confirm your email:</h2>

    <a href='{confirm_url}'> {confirm_url}</a>
    '''
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
        html_message=html_message,
    )

@shared_task(queue='mailing')
def confirm_unsubscribe_mail(email):
    from django.core import signing
    from django.urls import reverse
    token = signing.dumps({'email': email})
    confirm_url = f'{settings.SITE_URL}{reverse('mailing:unsubscribe_confirm', kwargs={'token': token,})}'
    subject = 'Unsubscribe Email'
    message = f'''
    Hello {email},

    Please click the link below to unsubscribe your email:
    {confirm_url}
    '''

    html_message = f'''
    <h2>Please click the link below to unsubscribe your email:</h2>

    <a href='{confirm_url}'> {confirm_url}</a>
    '''
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
        html_message=html_message,
    )