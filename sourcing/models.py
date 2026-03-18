# sourcing/models.py

from django.db import models
from quality_match.models import Product
class Supplier(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Procurement(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="procurements")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    price_per_unit = models.FloatField()
    total_price = models.FloatField(blank=True, null=True)
    quality_score = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price_per_unit
        super().save(*args, **kwargs)