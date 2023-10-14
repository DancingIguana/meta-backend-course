from django.urls import path
from djoser.views import UserViewSet
from . import views

# User registration
urlpatterns = [
    path("category/", views.CategoryView.as_view()),
    path("category/<int:pk>", views.SingleCategoryView.as_view(),  name="category-detail"),
    path("menu-items/", views.MenuItemsView.as_view()),
    path("menu-items/<int:pk>", views.SingleMenuItemView.as_view()),
    path("groups/<str:group_name>/users/", views.UserGroupListView.as_view()),
    path("groups/<str:group_name>/users/<int:pk>", views.SingleGroupUserView.as_view()),
    path("cart/menu-items/", views.CartView.as_view()),
    path("cart/menu-items/<int:pk>", views.SingleCartItemView.as_view()),
    path("orders/", views.OrdersView.as_view()),
    path("orders/<int:pk>", views.SingleOrderView.as_view()),
]