from django.core.management.base import BaseCommand
from products.scraper import scrape_products

class Command(BaseCommand):
    help = 'Scrape products from the website and store them in the database'

    def handle(self, *args, **kwargs):
        scrape_products()
        self.stdout.write(self.style.SUCCESS('Successfully scraped products'))
