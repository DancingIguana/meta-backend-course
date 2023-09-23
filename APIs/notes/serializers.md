# Serializers
## Definition
Serializers have two main purposes: 

- **Serialization**: Pulling data from the Django's DRF models and giving it to the clients. 
$$
Models/Objects \rightarrow Serialization \rightarrow JSON/XML/Other
$$

- **Deserialization**: Convert user supplied data into models to store them in the database by parsing the object (such as JSON or XML).

$$
 JSON/XML/Other \rightarrow Deserialization \rightarrow Django/DRF/Models
$$

## Implementation
### Structure
#### Basic Serializer 
Create a file called `serializers.py` at app-level and use this basic structure.

```py
from rest_framework import serializers

class MyBasicSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
```

You must make sure that the variables are a subset of the ones you have in the model you're going to be using.

```py
class BasicItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.SmallIntegerField()
```

#### Model Serializer
A model serializer simply pulls the necessary data from the model you're going to be referencing. Without needing to explicitly define the variables.

```py
class MyModelSerializer(serializers.ModelSerializer):
    # Change name of variable in API: inventory -> stock
    stock = serializers.IntegerField(source="inventory")
    # Add field based on class method
    price_after_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = models.MenuItem
        fields = ["id", "title", "price", "stock", "price_after_tax", "category", "category_id"]
    
    def calculate_tax(self, product:models.MenuItem):
        return product.price * Decimal(1.1)
```

In this example we can see some extra features you can implement with the serializer. Such as changing the name of a field, or adding a field based on a method.

### Serialization
When performing serialization, you can do it under the `views.py` functions.

#### GET Method

You have to serialize the item by simply calling the serializer over the model's objects and return it as a response.
```py
@api_view()
def menu_items(request):
    if request.method == "GET":
        items = models.MenuItem.objects.all()
        serialized_item = serializers.MenuItemSerializer(items, many=True)
        return Response(serialized_item.data)
```

### Deserialization

#### POST Method
Serialize the request with the serializer, validate it, save it and return the response.
```py
@api_view(["POST"])
def menu_items(request):
     if request.method == "POST":
        serialized_item = serializers.MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)
```

#### PUT/PATCH Method
It's basically the same as the POST method, but you have to specify that the fields
```py
@api_view(["PUT","PATCH"])
def single_item(request,id):
    item = get_object_or_404(models.MenuItem,pk=id)
    if request.method in ["PUT", "PATCH"]:
        serialized_item = serializers.MenuItemSerializer(item, data=request.data, partial=True)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_200_OK)
```

### Generics
One way more simple way to use these methods with the serializers is by using the `generics` module from the `rest_framework` library. Here's an example:

```py
from rest_framework import generics
from . import serializers, models

class MenuItemsView(generics.ListCreateAPIView):
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializers

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializers
```