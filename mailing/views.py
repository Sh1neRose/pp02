from django.shortcuts import render
from django.views import View
from .forms import SubscriberForm


class subscribe(View):
    def post(self, request, *args, **kwargs):
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'mailing/success.html')
        return render(request, 'mailing/cancel.html')
