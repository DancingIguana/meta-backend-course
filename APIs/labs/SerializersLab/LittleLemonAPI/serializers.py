from rest_framework import serializers
from . import models

class MenuItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.MenuItem
        fields = ["id", "title","price","inventory"]