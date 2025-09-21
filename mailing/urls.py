from django.urls import path, include
from . import views

app_name = 'mailing'

urlpatterns = [
    path('subscribe/', include([
        path('', views.subscribe.as_view(), name='subscribe'),
        path('<token>/', views.subscribe_confirm.as_view(), name='subscribe_confirm')
    ])),
    path('unsubscribe/', include([
        path('', views.unsubscribe.as_view(), name='unsubscribe'),
        path('<token>/', views.unsubscribe_confirm.as_view(), name='unsubscribe_confirm')
    ]))
]
