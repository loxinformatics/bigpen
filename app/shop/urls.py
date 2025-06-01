from django.shortcuts import render
from django.urls import path

from .views import ItemDetailView, ShopDashboard, place_order

# app_name = "shop"

urlpatterns = [
    path("items/", ShopDashboard, name="shop-dashboard"),
    path("items/<int:pk>/", ItemDetailView, name="item-detail"),
    path("place-order/", place_order, name="place_order"),
    path(
        "order-success/",
        lambda r: render(r, "shop/order_success.html"),
        name="order_success",
    ),
]
