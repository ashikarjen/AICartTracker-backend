from django.db import models

class Product(models.Model):
    daraz_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    price = models.FloatField(null=True, blank=True)
    url = models.TextField()
    details = models.TextField(null=True, blank=True)
    rating = models.CharField(max_length=50, null=True, blank=True)
    image_urls = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    reviewer_name = models.CharField(max_length=255)
    rating = models.IntegerField()
    content = models.TextField()
    sentiment = models.CharField(max_length=10)  # Positive, Negative, Neutral
    date_posted = models.DateField()

    def __str__(self):
        return f'Review for {self.product.name} by {self.reviewer_name}'
