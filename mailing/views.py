from django.shortcuts import render
from django.views import View
from .forms import SubscribeForm, UnsubscribeForm
from .tasks import confirm_subscribe_mail, confirm_unsubscribe_mail
from django.core import signing
from .models import Subscriber
from django.contrib import messages


class subscribe(View):
    def post(self, request, *args, **kwargs):
        form = SubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            if subscriber.is_active == True:
                return render(request, 'mailing/cancel.html')
            confirm_subscribe_mail.delay(email)
            return render(request, 'mailing/success.html')
        return render(request, 'mailing/cancel.html')
    
class subscribe_confirm(View):
    def get(self, request, token, *args, **kwargs):
        try:
            email = signing.loads(token, max_age=3600)['email']
            subscriber = Subscriber.objects.get(email=email)
        except (TypeError, ValueError, Subscriber.DoesNotExist):
            subscriber = None

        if subscriber:
            subscriber.is_active = True
            subscriber.save()
            return render(request, 'mailing/success.html')
        return render(request, 'mailing/cancel.html')
    
class unsubscribe(View):
    def get(self, request, *args, **kwargs):
        form = UnsubscribeForm()
        return render(request, 'mailing/unsubscribe.html', {
            'form': form,
        })
    def post(self, request, *args, **kwargs):
        form = UnsubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                subscriber = Subscriber.objects.get(email=email)
            except (TypeError, ValueError, Subscriber.DoesNotExist):
                subscriber = None
            if subscriber:
                messages.success(request, 'Please check your email.')
                confirm_unsubscribe_mail.delay(email)
                return render(request, 'mailing/success.html')
            messages.warning(request, 'There is no such email.')
        else:
            messages.error(request, 'Please enter a valid email address.')
        form = UnsubscribeForm()
        return render(request, 'mailing/cancel.html', {
            'form': form,
        })

class unsubscribe_confirm(View):
    def get(self, request, token, *args, **kwargs):
        try:
            email = signing.loads(token, max_age=3600)['email']
            subscriber = Subscriber.objects.get(email=email)
        except (TypeError, ValueError, Subscriber.DoesNotExist):
            subscriber = None

        if subscriber:
            subscriber.is_active = False
            subscriber.save()
            return render(request, 'mailing/success.html')
        return render(request, 'mailing/cancel.html')