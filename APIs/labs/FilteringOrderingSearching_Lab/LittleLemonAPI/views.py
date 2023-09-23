from rest_framework import generics
from . import models, serializers

class CategoriesView(generics.ListCreateAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

class MenuItemsView(generics.ListCreateAPIView):
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer
    ordering_fields = ["price", "inventory"]
    filterset_fields = ["price", "inventory"]
    search_fields = ["title"]
    