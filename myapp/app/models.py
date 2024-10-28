
from django.db import models

class Product(models.Model):
    product = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity=models.IntegerField(null=True)
    def __str__(self):
        return self.product

