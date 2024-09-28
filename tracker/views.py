from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product
from .nlp_utils import extract_url, get_intent
from .serializers import ProductSerializer
from .tasks import update_product_info
from rest_framework.views import APIView
from .scraper import scrape_daraz_product

import re

def extract_daraz_id(url):
    match = re.search(r'-i(\d+)-s', url)
    return match.group(1) if match else None

class NaturalLanguageInputView(APIView):
    def post(self, request):
        user_input = request.data.get('text')
        if not user_input:
            return Response({'error': 'No text provided.'}, status=400)

        # Extract URL(s) from the input text
        urls = extract_url(user_input)
        if not urls:
            return Response({'error': 'No URL found in the input.'}, status=400)

        # Recognize user intent
        intent = get_intent(user_input)

        if intent == "track_product":
            # Proceed with tracking logic
            product_url = urls[0]  # Assuming the first URL is the product URL
            
            # Call the scrape function directly
            scrape_view = ProductViewSet()
            scrape_request_data = {'url': product_url}
            scrape_response = scrape_view.scrape(scrape_request_data)

            return scrape_response
        else:
            return Response({'error': 'Unknown intent.'}, status=400)


class ProductViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving products.
    """

    def list(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def scrape(self, request):
        url = request.get('url')
        if not url:
            return Response({'error': 'URL is required.'}, status=status.HTTP_400_BAD_REQUEST)

        daraz_id = extract_daraz_id(url)
        if not daraz_id:
            return Response({'error': 'Invalid Daraz product URL.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the product already exists
        try:
            product = Product.objects.get(daraz_id=daraz_id)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            # Scrape the product data
            product_data = scrape_daraz_product(url)
            if not product_data:
                return Response({'error': 'Failed to scrape product data.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Save the product data
            serializer = ProductSerializer(data=product_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def bookmark(self, request, pk=None):
        # Implement bookmarking logic here
        # For now, we'll assume bookmarking is handled client-side or via another model
        return Response({'status': f'Product {pk} bookmarked for tracking.'})
    
    @action(detail=True, methods=['get'])
    def more_info(self, request, pk=None):
        # Implement logic to fetch more info from the web
        product = Product.objects.get(pk=pk)
        # Start task to fetch more info
        update_product_info.delay(product.id)
        return Response({'status': 'Fetching additional information.'})

