from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product

class NaturalLanguageInputViewTest(APITestCase):

    def test_nlp_track_product(self):
        """
        Test the NLP endpoint with a product tracking intent.
        """
        url = reverse('nlp-input')
        data = {'text': 'I want to track the product, here is the product url: https://www.daraz.com.bd/products/45-44-41-40-38-42-9-8-7-6-se-5-3-4-i393542251-s1960698080.html?pvid=b25bc834-9266-495d-b45b-71380b86a04e&search=jfy&scm=1007.28811.376629.0&priceCompare=skuId%3A1960698080%3Bsource%3Atpp-recommend-plugin-41701%3Bsn%3Ab25bc834-9266-495d-b45b-71380b86a04e%3BunionTrace%3A2151e22017274566653064040e52ec%3BoriginPrice%3A27400%3BvoucherPrice%3A27400%3BdisplayPrice%3A27400%3BsourceTag%3A%23auto_collect%231%24auto_collect%24%3BsinglePromotionId%3A50000022812038%3BsingleToolCode%3AshopPromPrice%3BvoucherPricePlugin%3A1%3BbuyerId%3A0%3ButdId%3A-1%3Btimestamp%3A1727456665428&spm=..just4u.d_393542251'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(daraz_id='393542251').exists())

    def test_nlp_invalid_intent(self):
        """
        Test the NLP endpoint with an unknown intent.
        """
        url = reverse('nlp-input')
        data = {'text': 'This is a random text without a known intent.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Unknown intent.', response.data['error'])


class ProductViewSetTest(APITestCase):

    def test_scrape_valid_url(self):
        """
        Test scraping a valid product URL.
        """
        url = reverse('product-scrape')
        data = {'url': 'https://www.daraz.com.bd/products/45-44-41-40-38-42-9-8-7-6-se-5-3-4-i393542251-s1960698080.html?pvid=b25bc834-9266-495d-b45b-71380b86a04e&search=jfy&scm=1007.28811.376629.0&priceCompare=skuId%3A1960698080%3Bsource%3Atpp-recommend-plugin-41701%3Bsn%3Ab25bc834-9266-495d-b45b-71380b86a04e%3BunionTrace%3A2151e22017274566653064040e52ec%3BoriginPrice%3A27400%3BvoucherPrice%3A27400%3BdisplayPrice%3A27400%3BsourceTag%3A%23auto_collect%231%24auto_collect%24%3BsinglePromotionId%3A50000022812038%3BsingleToolCode%3AshopPromPrice%3BvoucherPricePlugin%3A1%3BbuyerId%3A0%3ButdId%3A-1%3Btimestamp%3A1727456665428&spm=..just4u.d_393542251'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(daraz_id='393542251').exists())

    def test_scrape_invalid_url(self):
        """
        Test scraping an invalid product URL.
        """
        url = reverse('product-scrape')
        data = {'url': 'https://www.invalid-url.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid Daraz product URL.', response.data['error'])

    def test_scrape_missing_url(self):
        """
        Test scraping without providing a URL.
        """
        url = reverse('product-scrape')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('URL is required.', response.data['error'])
