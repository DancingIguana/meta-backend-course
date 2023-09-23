from rest_framework import serializers
from . import models

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MenuItem
        fields = ["id","title","price","inventory"]
        extra_kwargs = {
            "price": {"min_value":2},
            "inventory": {"min_value":0}
        }