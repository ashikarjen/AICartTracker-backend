from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    daraz_id = models.CharField(max_length=100, unique=True)
    url = models.URLField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    last_checked = models.DateTimeField(auto_now=True)
    summary = models.TextField(blank=True, null=True)
    image_urls = models.JSONField(blank=True, null=True)

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
