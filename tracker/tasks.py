from celery import shared_task
from .models import Product, Review
import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from .nlp_utils import analyze_sentiment
from .scraper import scrape_daraz_product, scrape_daraz_reviews

@shared_task
def scrape_product_data(url):
    # Scrape product data using Selenium
    product_data = scrape_daraz_product(url)
    if not product_data:
        # Handle error
        return
    product, created = Product.objects.update_or_create(
        daraz_id=product_data['daraz_id'],
        defaults=product_data
    )
    # Scrape reviews
    scrape_reviews_for_product.delay(product.id)
    # Analyze reviews
    analyze_product_reviews.delay(product.id)


@shared_task
def analyze_product_reviews(product_id):
    product = Product.objects.get(id=product_id)
    reviews = product.reviews.all()
    sentiments = []
    for review in reviews:
        sentiment = analyze_sentiment(review.content)
        review.sentiment = sentiment
        review.save()
        sentiments.append(sentiment)
    # Update product summary based on sentiments
    product.summary = generate_product_summary(sentiments)
    product.save()

@shared_task
def update_product_info(product_id):
    # Implement logic to fetch more info from the web
    pass

@shared_task
def scheduled_product_updates():
    # Query all bookmarked products and update their data
    products = Product.objects.all()  # Modify this to filter bookmarked products
    for product in products:
        scrape_product_data.delay(product.url)
