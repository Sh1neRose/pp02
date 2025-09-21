from .forms import SubscriberForm
def subscriberform(request):
    return {'subscriberform': SubscriberForm}