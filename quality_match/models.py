from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ReferenceQualityImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reference_images")
    image = models.ImageField(upload_to="reference_images/")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class QualityCheck(models.Model):

    RESULT_CHOICES = [
        ("GOOD", "Good"),
        ("ACCEPTABLE", "Acceptable"),
        ("REJECT", "Reject"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    uploaded_image = models.ImageField(upload_to="quality_checks/")
    
    match_score = models.FloatField(blank=True, null=True)
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, blank=True, null=True)

    ai_response = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)