# quality/models.py

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class QualityParameter(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="parameters")
    name = models.CharField(max_length=100)  # e.g. Color, Size, Freshness
    min_value = models.FloatField()
    max_value = models.FloatField()
    ideal_value = models.FloatField()

    def __str__(self):
        return f"{self.product.name} - {self.name}"


class QualityCheck(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier_name = models.CharField(max_length=120)
    score = models.FloatField()
    grade = models.CharField(max_length=10)  # A / B / C
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)