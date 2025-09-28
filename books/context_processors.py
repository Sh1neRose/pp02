from .forms import Search

def searchform(request):
    return {'searchform': Search,}