from rest_framework.permissions import BasePermission
    
class IsAdminOrManagerPermission(BasePermission):
    def has_permission(self,request,view):
        return request.user.is_staff or request.user.groups.filter(name="Manager").exists()

class IsCustomerPermission(BasePermission):
    def has_permission(self, request, view):
        return not request.user.groups.exists() and not request.user.is_staff # If it has a group, it is not a customer, admin is not a customer

class IsDeliveryCrewPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Delivery crew").exists()

class IsAdminManagerOrDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.user.groups.filter(name="Manager").exists() or request.user.groups.filter(name="Delivery crew").exists()
    
class OrderPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        # Check if the user is in the "Delivery crew" group
        if user.groups.filter(name="Delivery crew").exists():
            restricted_fields = ["id", "user", "delivery_crew", "total", "date", "order_items"]  # Add the field names you want to restrict
            if request.method in ["PATCH", "PUT"]:
                for field in restricted_fields:
                    if field in request.data and request.data[field] != getattr(obj, field):
                        return False
                    
        # Check if the user is in the "Delivery crew" group
        if user.groups.filter(name="Manager").exists() or user.is_staff:
            restricted_fields = ["id", "user", "total", "date", "order_items"]  # Add the field names you want to restrict
            if request.method in ["PATCH", "PUT"]:
                for field in restricted_fields:
                    if field in request.data and request.data[field] != getattr(obj, field):
                        return False

        return True