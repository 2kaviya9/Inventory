from django.test import TestCase
from inventory_app.models import Category, Supplier, InventoryItem

class InventoryItemModelTest(TestCase):

    def setUp(self):
        """Create a category, a supplier, and an inventory item for testing."""
        self.category = Category.objects.create(name='Electronics', description='Devices and gadgets')
        self.supplier = Supplier.objects.create(name='Tech Supplier', contact_info='techsupplier@example.com')
        
        self.item = InventoryItem.objects.create(
            name='Smartphone',
            sku='SP123',
            category=self.category,
            supplier=self.supplier,
            description='Latest model smartphone',
            quantity=10,
            price=699.99
        )

    def test_inventory_item_creation(self):
        """Test if the inventory item is created successfully."""
        self.assertEqual(self.item.name, 'Smartphone')
        self.assertEqual(self.item.sku, 'SP123')
        self.assertEqual(self.item.category, self.category)
        self.assertEqual(self.item.supplier, self.supplier)
        self.assertEqual(self.item.description, 'Latest model smartphone')
        self.assertEqual(self.item.quantity, 10)
        self.assertEqual(self.item.price, 699.99)

    def test_inventory_item_str(self):
        """Test the string representation of the inventory item."""
        self.assertEqual(str(self.item), 'Smartphone (SP123)')

    def test_inventory_item_price_decimal(self):
        """Test if the price is stored as a decimal."""
        self.assertIsInstance(self.item.price, float)

   