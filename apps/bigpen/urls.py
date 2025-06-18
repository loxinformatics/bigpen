from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

api = DefaultRouter()
api.register(r"portfolio", views.PortfolioViewSet)

urlpatterns = [
    path("api/", include(api.urls)),
    path("", views.Portfolio.as_view(), name="dashboard"),
    path("contact", views.ContactView.as_view(), name="contact"),
]
