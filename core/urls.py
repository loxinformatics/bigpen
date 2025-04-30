from django.urls import path

from .views import robots_txt, home

urlpatterns = [
    path("robots.txt", robots_txt, name="robots_txt"),
    path("", home, name="homepage"),
    path("", home, name="store"),
]
