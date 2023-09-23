from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers

@api_view(["GET","POST"])
def menu_items(request):
    if request.method == "GET":
        items = models.MenuItem.objects.all()
        serialized_item = serializers.MenuItemSerializer(items, many=True)
        return Response(serialized_item.data)
    if request.method == "POST":
        serialized_item = serializers.MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)


@api_view(["GET", "PATCH"])
def single_item(request,id):
    item =get_object_or_404(models.MenuItem,pk=id)

    if request.method == "GET":
        serialized_item = serializers.MenuItemSerializer(item)
        return Response(serialized_item.data)
    if request.method =="PATCH":
        serialized_item = serializers.MenuItemSerializer(item, data=request.data, partial=True)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_200_OK)
