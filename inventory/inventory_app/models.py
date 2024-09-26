from django.db import models
from django.core.exceptions import ValidationError

class Category(models.Model):
    """Represents a product category."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    """Represents the supplier of inventory items."""
    name = models.CharField(max_length=100)
    contact_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    """Represents an item in the inventory."""
    name = models.CharField(max_length=255, unique = True)
    sku = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.quantity < 0:
            raise ValidationError('Quantity must be a non-negative integer.')


    def __str__(self):
        return f'{self.name} ({self.sku})'

    class Meta:
        verbose_name = 'Inventory Item'
        verbose_name_plural = 'Inventory Items'

    
