from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.home import ContactView, FeaturesView, LandingView, PortfolioView
from .views.stock import CategoryViewSet, ItemDetailView

api = DefaultRouter()
api.register(r"portfolio", CategoryViewSet)

urlpatterns = [
    path("", LandingView.as_view(), name="landing"),
    path("products", PortfolioView.as_view(), name="portfolio"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("features", FeaturesView.as_view(), name="features"),
    path("api/", include(api.urls)),
    path(
        "swaps/portfolio/item/<int:id>/",
        ItemDetailView.as_view(),
        name="item-detail",
    ),
]
