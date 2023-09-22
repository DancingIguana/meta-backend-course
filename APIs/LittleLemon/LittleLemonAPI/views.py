from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import models

@api_view()
def menu_items(request):
    items = models.MenuItem.objects.all()
    return Response(items.values())
