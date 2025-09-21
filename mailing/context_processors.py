from .forms import SubscribeForm 
def subscriberform(request):
    return {'subscribeform': SubscribeForm}