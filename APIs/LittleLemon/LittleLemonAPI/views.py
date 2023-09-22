from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import models, serializers

@api_view()
def menu_items(request):
    items = models.MenuItem.objects.all()
    serialized_item = serializers.MenuItemSerializer(items, many=True)

    return Response(serialized_item.data)


@api_view()
def single_item(request,id):
    item =get_object_or_404(models.MenuItem,pk=id)
    serialized_item = serializers.MenuItemSerializer(item)
    return Response(serialized_item.data)
