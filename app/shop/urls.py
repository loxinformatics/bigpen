from django.urls import path

from .views import ShopDashboard

urlpatterns = [path("", ShopDashboard, name="shop-dashboard")]
