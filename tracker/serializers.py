from rest_framework import serializers
from .models import Product, Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['reviewer_name', 'rating', 'content', 'sentiment', 'date_posted']

class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'daraz_id', 'url', 'price', 'last_checked', 'summary', 'image_urls', 'reviews']
