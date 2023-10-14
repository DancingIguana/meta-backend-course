from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers, exceptions
from . import models, permissions


class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id','title']


class MenuItemSerializer(serializers.ModelSerializer):
    # Decided to display the title and id instead of just the id.
    # It makes it way more readable
    category = CategorySerializer(read_only =True) 
    category_id = serializers.IntegerField(write_only=True) 
    class Meta:
        model = models.MenuItem
        fields = [
            "id", 
            "title", 
            "price", 
            "featured", 
            "category",
            "category_id",
        ]

    # To avoid server error when having invalid foreign keys
    def validate_category_id(self, value):
        try:
            category = models.Category.objects.get(pk=value)
            return value
        except models.Category.DoesNotExist:
            raise serializers.ValidationError("Category with this ID does not exist.")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        ]


class AddUserToGroupSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    username = serializers.CharField(required=False)
    # We must either validate by id or by username
    def validate(self, data):
        id = data.get("id")
        username = data.get("username")

        if not id and not username:
            raise serializers.ValidationError("Either 'id' or 'username' must be provided")
        
        # Check that the id and username belong to the same person
        if id and username:
            user_by_id = get_object_or_404(User,pk=id)
            user_by_username = get_object_or_404(User,username=username)
            if user_by_id != user_by_username:
                raise serializers.ValidationError(f"User with id {id} doesn't have the username {username}. Provide only one of the two fields, or make them match properly.")

        return data


class MenuItemForCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MenuItem
        fields = [
            "id",
            "title",
            "price",
        ]


class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemForCartSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2,read_only=True)   
    
    class Meta:
        model = models.Cart
        fields = [
            "id",
            "menuitem",
            "menuitem_id",
            "quantity",
            "price",
        ]


    def create(self, validated_data):
        user = self.context["request"].user

        # Check if the user is authenticated
        if not user.is_authenticated:
            raise exceptions.PermissionDenied("User must be authenticated")
        

        
        menuitem_id = validated_data.get("menuitem_id")

        # Check if a cart item with the same menuitem_id already exists for the user
        existing_cart_item = models.Cart.objects.filter(user=user, menuitem_id=menuitem_id).first()

        if existing_cart_item:
            raise exceptions.ValidationError("This menu item is already in the cart.")
        

        # Get the menuitem and pass it to the cart
        menuitem_object = get_object_or_404(models.MenuItem, pk=validated_data.get("menuitem_id"))
        
        quantity = validated_data.get("quantity")
        unit_price = menuitem_object.price
        price = quantity*unit_price
        
        
        validated_data["user"] = user
        validated_data["price"] = price
        cart = models.Cart.objects.create(**validated_data)

        return cart
    
    def update(self, instance, validated_data):
        new_quantity = validated_data.get("quantity", instance.quantity)
        menuitem_object = get_object_or_404(models.MenuItem, pk=instance.menuitem_id)
        unit_price = menuitem_object.price
        new_price = new_quantity * unit_price

        instance.quantity = new_quantity
        instance.price = new_price
        instance.save()

        return instance


class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemForCartSerializer(read_only=True)
    class Meta:
        model = models.OrderItem
        fields = [
            "id",
            "menuitem",
            "quantity",
            "price"
        ]


class SingleOrderSerializerForCustomer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    delivery_crew = UserSerializer(read_only=True)
    #user = UserSerializer(read_only=True)
    class Meta:
        model = models.Order
        fields = [
            "id",
            #"user", # user not necessary to specify when the same user is requesting
            "delivery_crew",
            "status",
            "total",
            "date",
            "order_items",
        ]
        read_only_fields = fields


# For managers only editing delivery crew and status
class SingleOrderSerializerForManager(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = models.Order
        fields = [
            "id",
            "user",
            "delivery_crew",
            "status",
            "total",
            "date",
            "order_items",
        ]
        read_only_fields = ["id","user","total","date",]

    # Change the reperesentation of delivery crew only in GET method
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context["request"].method == "GET":
            data["delivery_crew"] = UserSerializer(instance.delivery_crew).data
        return data


# For delivery crew only editing status
class SingleOrderSerializerForDeliveryCrew(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = models.Order
        fields = [
            "id",
            #"delivery_crew", # delivery crew not necessary when the same crew is checking
            "user",
            "status",
            "total",
            "date",
            "order_items",
        ]
        read_only_fields = ["id","user","total","date","order_items"]

    
