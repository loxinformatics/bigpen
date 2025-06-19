from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

api = DefaultRouter()
api.register(r"portfolio", views.CategoryViewSet)

urlpatterns = [
    path("", views.LandingView.as_view(), name="landing"),
    path("api/", include(api.urls)),
    path(
        "swaps/portfolio/item/<int:id>/",
        views.ItemDetailView.as_view(),
        name="item-detail",
    ),
]
