from django.core.management.base import BaseCommand
from products.daraz import DarazScraper

class Command(BaseCommand):
    help = 'Scrapes products from Daraz and saves them to an Excel file'

    def handle(self, *args, **kwargs):
        scraper = DarazScraper()
        scraper.scrape_products()
