from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.booksview.as_view(), name='books'),
    path('searchbook/', views.searchview.as_view(), name='searchbook'),
    path('<slug:slug>/', views.booksview.as_view(), name='books_by_genre'),
    path('book/<int:id>/', views.bookview.as_view(), name='book'),
]
