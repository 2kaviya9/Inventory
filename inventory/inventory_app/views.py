from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import InventoryItem, Category, Supplier
from inventory_app.serializers import InventoryItemSerializer, CategorySerializer, SupplierSerializer
from django.core.cache import cache
import logging

# Get the custom logger
logger = logging.getLogger('inventory_app')

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        item_id = kwargs['pk']

        # Log the start of the process at the DEBUG level
        logger.debug(f"Attempting to retrieve item with ID: {item_id}")

        # Check if the item is cached
        cached_item = cache.get(f'inventory_item_{item_id}')
        if cached_item:
            # Log successful retrieval at the INFO level
            logger.info(f"Item {item_id} retrieved successfully from cache.")
            return Response(cached_item)

        try:
            # Call the superclass method to retrieve the item from the database
            response = super().retrieve(request, *args, **kwargs)

            # Cache the response data for future requests
            cache.set(f'inventory_item_{item_id}', response.data, timeout=300)

            return response
        except InventoryItem.DoesNotExist:
            # Log error if the item is not found
            logger.error(f"Item with ID {item_id} does not exist.")
            return Response({"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:

            # Log any unexpected errors
            logger.error(f"An unexpected error occurred while retrieving item {item_id}: {str(e)}")
            return Response({"detail": "An error occurred."}, status=status.HTTP_404_NOT_FOUND)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
