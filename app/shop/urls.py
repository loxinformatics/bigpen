from django.urls import path
from .views import ShopDashboard, ItemDetailView

urlpatterns = [
    path("items/", ShopDashboard, name="shop-dashboard"),
    path("items/<int:pk>/", ItemDetailView, name="item-detail"),
]
