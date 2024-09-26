from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from inventory_app.models import InventoryItem, Category
from inventory_app.tests.test_setup import TestSetup
from users.models import User

class InventoryTests(TestSetup):

    def setUp(self):
        self.user1 = User.objects.create(email="testuser1@gmail.com", password="##password")
        
        self.category = Category.objects.create(name='Electronics')
        self.item_data = {
            'name': 'Laptop',
            'sku': 'LPT123',
            'category': self.category.id,
            'quantity': 10,
            'price': '1200.00'
        }
        return super().setUp()
    

    def test_authorized_user_can_view_item(self):
        """Test Authorized User can list Item."""
        response = self.client.get(
            reverse("inventoryitem-list"), format="json", HTTP_AUTHORIZATION=self.user
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_user_can_view_item(self):
        """Test UnAuthorized User cannot  list Item."""
        response = self.client.get(
            reverse("inventoryitem-list"), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_authorized_user_can_create_item(self):
        """Test Authorized User can create  Item."""
        data =  {"name":'Smartphone',
            "sku":'SP123',
            "category":self.category.pk,
            "description":'Latest model smartphone',
            "quantity":10,
            "price":699.99}
        response = self.client.post(
            reverse("inventoryitem-list"), data, format="json", HTTP_AUTHORIZATION=self.user
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthorized_user_cannot_create_item(self):
        """Test UnAuthorized User cannot create Item."""
        data =  {"name":'Smartphone',
            "sku":'SP123',
            "category":self.category.pk,
            "description":'Latest model smartphone',
            "quantity":10,
            "price":699.99}
        response = self.client.post(
            reverse("inventoryitem-list"), data, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_user_can_updae_item(self):
        """Test Authorized User can update Item."""
        self.item = InventoryItem.objects.create(
            name='Smartphone',
            sku='SP123',
            category=self.category,
            description='Latest model smartphone',
            quantity=10,
            price=699.99
        )

        data =  {"name":'Smartphone',
            "sku":'SP123',
            "category":self.category.pk,
            "description":'Latest model smartphone',
            "quantity":10,
            "price":699.99}
        response = self.client.put(
            reverse("inventoryitem-detail", kwargs={"pk": self.item.pk}), data, format="json", HTTP_AUTHORIZATION=self.user
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_user_cannot_updae_item(self):
        """Test UnAuthorized User canot update  Item."""
        self.item = InventoryItem.objects.create(
            name='Smartphone',
            sku='SP123',
            category=self.category,
            description='Latest model smartphone',
            quantity=10,
            price=699.99
        )

        data =  {"name":'Smartphone',
            "sku":'SP123',
            "category":self.category.pk,
            "description":'Latest model smartphone',
            "quantity":10,
            "price":699.99}
        response = self.client.put(
            reverse("inventoryitem-detail", kwargs={"pk": self.item.pk}), data, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_authorized_user_can_delete_item(self):
        """Test Authorized User can delete Item."""
        self.item = InventoryItem.objects.create(
            name='Smartphone',
            sku='SP123',
            category=self.category,
            description='Latest model smartphone',
            quantity=10,
            price=699.99
        )
        response = self.client.delete(
            reverse("inventoryitem-detail", kwargs={"pk": self.item.pk}), format="json", HTTP_AUTHORIZATION=self.user
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthorized_user_cannot_delete_item(self):
        """Test Authorized User can Update  Item."""
        self.item = InventoryItem.objects.create(
            name='Smartphone',
            sku='SP123',
            category=self.category,
            description='Latest model smartphone',
            quantity=10,
            price=699.99
        )
        response = self.client.delete(
            reverse("inventoryitem-detail", kwargs={"pk": self.item.pk}), format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

 
 

