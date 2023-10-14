import datetime
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, exceptions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models, serializers, permissions, utils


"""
----------------------CATEGORIES----------------------
Note: Not specified in the endpoints of the project, but I consider them necessary.

Permissions: 
- GET: All authenticated users
- POST, PATCH and DELETE: only the admin
"""

class CategoryView(generics.ListCreateAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()] 
        return [IsAuthenticated()]


class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminUser()]

"""
----------------------MENU ITEMS----------------------
Permissions: 
- GET: All authenticated users
- POST, PATCH and DELETE: Admin and Managers
"""


class MenuItemsView(generics.ListCreateAPIView):
    serializer_class = serializers.MenuItemSerializer
    ordering_fields = ["price"]
    filterset_fields = ["category__title","featured"] 
    search_fields = ["title"]

    def get_queryset(self):
        queryset = models.MenuItem.objects.select_related("category").all()
        category_title = self.request.query_params.get("category")
        featured = self.request.query_params.get("featured")
        if category_title:
            queryset = queryset.filter(category__title = category_title)
        if featured:
            queryset = queryset.filter(featured=featured)
        return queryset
    
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), permissions.IsAdminOrManagerPermission()]
        return [IsAuthenticated()]
    
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAuthenticated(), permissions.IsAdminOrManagerPermission()]


"""
----------------------USER GROUPS----------------------
It allows to search, post or update the group of users 
registered as managers or delivery crew.

PERMISSIONS: Only managers and admin for all actions.
"""

# Mapping the group name as specified in views.py 
# to how it's defined in the database
VIEW_GROUPNAME2DB_GROUPNAME = {
    "manager": "Manager",
    "delivery-crew": "Delivery crew"
}
class UserGroupListView(APIView):
    permission_classes = [permissions.IsAdminOrManagerPermission]
    serializer_class = serializers.AddUserToGroupSerializer
    
    def get(self, request, group_name):
        group = utils.get_group_or_404(group_name, VIEW_GROUPNAME2DB_GROUPNAME)
        users = User.objects.filter(groups=group)
        serialized_users = serializers.UserSerializer(users,many=True)
        return Response(serialized_users.data,status=status.HTTP_200_OK)

    def post(self, request, group_name):
        group = utils.get_group_or_404(group_name, VIEW_GROUPNAME2DB_GROUPNAME)
        serialized_data = self.serializer_class(data=request.data)

        if not serialized_data.is_valid():
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user_id = request.data.get("id")
        username = request.data.get("username")
        if user_id:
            user = get_object_or_404(User,pk=user_id)
        else:
            user = get_object_or_404(User,username=username)
        
        if group in user.groups.all(): 
            return Response({"message": f"User {user.username} already belongs to group {group.name}. No changes."}, status=status.HTTP_200_OK)
        
        user.groups.add(group)
        user.save()

        return Response(
            {"message": f"User {user.username} assigned to group {group.name} successfully"},
            status = status.HTTP_201_CREATED
        )


class SingleGroupUserView(APIView):
    permission_classes = [permissions.IsAdminOrManagerPermission]
    serializer_class = serializers.UserSerializer

    def get(self, request, group_name, pk):
        group = utils.get_group_or_404(group_name, VIEW_GROUPNAME2DB_GROUPNAME)
        user = get_object_or_404(User, pk=pk)
        if group not in user.groups.all():
            return Response(
                {"message": f"User {user.username} doesn't belong to group {group.name}"},
                status=status.HTTP_200_OK
            )
        
        serialized_user = self.serializer_class(user)
        return Response(
            serialized_user.data,
            status=status.HTTP_200_OK
        )


    def delete(self, request, group_name, pk):
        group = utils.get_group_or_404(group_name, VIEW_GROUPNAME2DB_GROUPNAME)
        user = get_object_or_404(User,pk=pk)
        if group not in user.groups.all():
            return Response(
                {"message": f"User {user.username} doesn't belong to group {group.name}"},
                status=status.HTTP_200_OK
            )
        user.groups.remove(group)
        user.save()
        return Response(
            {"message": f"User {user.username} removed from group {group.name}"},
            status=status.HTTP_200_OK
        )

"""
----------------------CART----------------------
Each customer, can add menu items to their own 
cart. 

Permissions:
GET, POST, PUT, PATCH, DELETE: Customers 
remove "request.user.is_staff" from permissions.IsCustomerPermission 
if you want to use admin for testing
"""

class CartView(APIView):
    serializer_class = serializers.CartSerializer
    permission_classes = [IsAuthenticated, permissions.IsCustomerPermission]

    def get(self, request):
        cart = models.Cart.objects.filter(user=request.user.id)
        serialized_cart = serializers.CartSerializer(cart,many=True)
        return Response(serialized_cart.data, status=status.HTTP_200_OK)

    def post(self, request):
        serialized_data = self.serializer_class(
            data=request.data, 
            context={"request":request}
        )
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user = request.user
        print("Hi")
        cart_items = models.Cart.objects.filter(user=user)
        cart_items.delete()

        return Response(
            {"message": "All the items in the cart have been deleted successfully"}, 
            status=status.HTTP_200_OK # If using 204, then no message appears
        )


class SingleCartItemView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CartSerializer
    permission_classes = [IsAuthenticated, permissions.IsCustomerPermission]
    def get_queryset(self):
        user = self.request.user
        queryset = models.Cart.objects.filter(user=user)
        return queryset
    

class OrdersView(generics.ListCreateAPIView):
    #serializer_class = serializers.OrderSerializer
    ordering_fields = ["total", "date"]
    filterset_fields = ["delivery_crew"]
    def get_queryset(self):
        queryset = models.Order.objects.all()
        # Manager
        if self.request.user.groups.filter(name="Manager").exists() or self.request.user.is_staff:
            pass
        # Customer
        elif not self.request.user.groups.exists():
            queryset = queryset.filter(user=self.request.user)
        # Delivery crew
        elif self.request.user.groups.filter(name="Delivery crew").exists():
            queryset = queryset.filter(delivery_crew = self.request.user)
        
        delivery_crew_id = self.request.query_params.get("delivery_crew_id")
        delivery_crew_username = self.request.query_params.get("delivery_crew_username")
        order_status = self.request.query_params.get("status")
        user_id = self.request.query_params.get("user_id")
        user_username = self.request.query_params.get("user_username")

        if delivery_crew_id:
            queryset = queryset.filter(delivery_crew__id = delivery_crew_id)

        if delivery_crew_username:
            queryset = queryset.filter(delivery_crew__username = delivery_crew_username)

        if order_status:
            if order_status not in ["True","1", "False", "0"]:
                raise exceptions.NotAcceptable("Status value must be either 'True' or '1' for true or 'False' or '0' for false.")
            
            queryset = queryset.filter(status=order_status)

        if user_id:
            queryset = queryset.filter(user__id = user_id)

        if user_username:
            queryset = queryset.filter(user__username = user_username)

        return queryset

    def post(self, request):
        # Get the items from the user's cart
        cart_objects = models.Cart.objects.filter(user=self.request.user)
        if len(cart_objects) == 0: 
            return Response({"message": "Can't create order, no items in cart"}, status=status.HTTP_200_OK)

        # Create the base order object
        order_data = {
            "user": self.request.user,
            "delivery_crew": None,
            "status": False,
            "total": 0,
            "date": datetime.date.today()
        }

        order_object = models.Order.objects.create(**order_data)


        # Pass the cart's items to the order's items
        for cart_object in cart_objects:
            order_item_dict = {
                "order": order_object,
                "menuitem": cart_object.menuitem,
                "quantity": cart_object.quantity,
                "price": cart_object.price,
            }
            models.OrderItem.objects.create(**order_item_dict)

        order_object.total = str(sum([obj.price for obj in cart_objects]))
        order_object.save()
        cart_objects.delete()
        return Response({"message": "Order created successfully"}, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        # Only customers can make the order
        if self.request.method == "POST":
            return [permissions.IsCustomerPermission()]
        # Only managers and delivery crew can update 
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        # Admin exclusive (can do what the manager, customer and delivery crew can)
        if self.request.user.groups.filter(name="Manager").exists() or self.request.user.is_staff:
            return serializers.SingleOrderSerializerForManager
        elif self.request.user.groups.filter(name="Delivery crew").exists():
            return serializers.SingleOrderSerializerForDeliveryCrew
        
        return serializers.SingleOrderSerializerForCustomer

            
class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        if self.request.user.groups.filter(name="Manager").exists() or self.request.user.is_staff:
            return models.Order.objects.all()
        elif self.request.user.groups.filter(name="Delivery crew").exists():
            return models.Order.objects.filter(delivery_crew = self.request.user)
        return models.Order.objects.filter(user=self.request.user)
        
    def get_serializer_class(self):
        # Admin exclusive (can do what the manager, customer and delivery crew can)
        if self.request.user.groups.filter(name="Manager").exists() or self.request.user.is_staff:
            return serializers.SingleOrderSerializerForManager
        elif self.request.user.groups.filter(name="Delivery crew").exists():
            return serializers.SingleOrderSerializerForDeliveryCrew
        
        return serializers.SingleOrderSerializerForCustomer
    
    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAuthenticated(), permissions.IsAdminOrManagerPermission(), permissions.OrderPermissions()]
        if self.request.method in ["PATCH", "PUT"]:
            return [IsAuthenticated(), permissions.IsAdminManagerOrDeliveryCrew(), permissions.OrderPermissions()]
        
        return [IsAuthenticated()]
