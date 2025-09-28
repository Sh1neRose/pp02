from celery import shared_task
from .models import Genre, Book, Author
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin
from decimal import Decimal
import re

base = "https://www.goodreads.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}

@shared_task(bind=True, queue='books')
def update_genres(self):
    url = urljoin(base, '/genres/list')
    lastpage=False
    while not lastpage:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')
        links = soup.find_all('a', class_='actionLinkLite')
        for link in links:
            path = link.get('href')
            genre_url = urljoin(base, path)
            parsed = urlparse(genre_url)
            slug = parsed.path.rstrip('/').split('/')[-1]
            name = link.get_text(strip=True)
            Genre.objects.get_or_create(name=name, slug=slug, url=genre_url)
        next_page = soup.find('a', rel='next')
        if next_page:
            path = next_page.get('href')
            url = urljoin(base, path)
        else:
            lastpage=True

@shared_task(bind=True, queue='books')
def update_books(self):
    genres = Genre.objects.all()
    for genre in genres:
        res = requests.get(genre.url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')
        containers = soup.find_all('div', class_='coverWrapper')
        for container in containers:
            link = container.find('a')
            path = link.get('href')
            book_url = urljoin(base, path)
            book_parsed = urlparse(book_url)
            book_goodreads_id = int(book_parsed.path.rstrip('/').split('/')[-1].split('.')[0].split('-')[0])
            if not Book.objects.filter(goodreads_id=book_goodreads_id).exists():
                res = requests.get(book_url, headers=headers)
                soup = BeautifulSoup(res.text, 'lxml')
                title = soup.find('h1', {'data-testid': 'bookTitle'}).get_text(strip=True)
                rating = Decimal(soup.find('div', class_='RatingStatistics__rating').get_text(strip=True))
                rating_count = int(re.sub(r'\D', '', soup.find('span', {'data-testid': 'ratingsCount'}).get_text(strip=True)))
                img_conatiner = soup.find('img', {'role': 'presentation'})
                img_url = img_conatiner.get('src')
                description = soup.find('span', class_='Formatted').get_text(strip=True)
                author_container = soup.find('span', {'data-testid': 'name'})
                author_name=author_container.get_text(strip=True)
                author_url = author_container.parent.get('href')
                author_parsed = urlparse(author_url)
                author_goodreads_id = int(author_parsed.path.rstrip('/').split('/')[-1].split('.')[0].split('-')[0])
                author, created = Author.objects.get_or_create(goodreads_id=author_goodreads_id, name=author_name)
                book = Book.objects.create(
                    goodreads_id=book_goodreads_id,
                    title=title,
                    description=description,
                    author=author,
                    rating=rating,
                    rating_count=rating_count,
                    img_url=img_url,
                )
                book_genre_containers = soup.find_all('span', class_='BookPageMetadataSection__genreButton') 
                for book_genre_container in book_genre_containers:
                    genre_link = book_genre_container.find('a')
                    genre_url = genre_link.get('href')
                    genre_parsed = urlparse(genre_url)
                    genre_slug = genre_parsed.path.rstrip('/').split('/')[-1]
                    genre_name = genre_link.find('span').get_text(strip=True)
                    book_genre, created = Genre.objects.get_or_create(
                        slug=genre_slug,
                        defaults={'name': genre_name, 'url': genre_url}
                    )
                    book.genres.add(book_genre)
