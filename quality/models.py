# quality/models.py

from django.db import models
from quality_match.models import Product

class QualityParameter(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="parameters")
    name = models.CharField(max_length=100)  # e.g. Color, Size, Freshness
    min_value = models.FloatField()
    max_value = models.FloatField()
    ideal_value = models.FloatField()

    def __str__(self):
        return f"{self.product.name} - {self.name}"