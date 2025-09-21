from django.urls import path
from . import views

app_name = 'mailing'

urlpatterns = [
    path("subscribe/", views.subscribe.as_view(), name="subscribe")
]
