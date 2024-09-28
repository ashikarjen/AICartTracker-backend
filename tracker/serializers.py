from rest_framework import serializers
from .models import Product, Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['reviewer_name', 'rating', 'content', 'sentiment', 'date_posted']

class ProductSerializer(serializers.ModelSerializer):
    image_urls = serializers.ListField(child=serializers.URLField(), allow_empty=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'daraz_id', 'price', 'url', 'details', 'rating', 'image_urls']
