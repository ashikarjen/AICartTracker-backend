from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    url = models.URLField(unique=True)
    description = models.TextField()
    tracked = models.BooleanField(default=False)

    def __str__(self):
        return self.name
