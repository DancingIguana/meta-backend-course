from decimal import Decimal
from rest_framework import serializers
from . import models
#class MenuItemSerializer(serializers.Serializer):
#    id = serializers.IntegerField()
#    title = serializers.CharField(max_length=255)
#    price = serializers.DecimalField(max_digits=6, decimal_places=2)
#    inventory = serializers.IntegerField()

class MenuItemSerializer(serializers.ModelSerializer):
    # Change name of variable in API: inventory -> stock
    stock = serializers.IntegerField(source="inventory")
    price_after_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    class Meta:
        model = models.MenuItem
        fields = ["id", "title", "price", "stock", "price_after_tax"]

    def calculate_tax(self, product:models.MenuItem):
        return product.price * Decimal(1.1)