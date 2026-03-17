# khata/models.py
from django.db import models

class Party(models.Model):
    PARTY_TYPE = (
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
    )

    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=15, blank=True, null=True)
    type = models.CharField(max_length=10, choices=PARTY_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.type})"


class KhataEntry(models.Model):
    ENTRY_TYPE = (
        ('credit', 'Credit'),  # they owe you
        ('debit', 'Debit'),    # you owe them
    )

    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name="entries")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPE)
    note = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.party.name} - {self.amount}"


class Payment(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
