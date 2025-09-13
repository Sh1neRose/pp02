from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news.as_view(), name='news'),
    path('<slug:slug>/', views.news.as_view(), name='news_by_category')
]
