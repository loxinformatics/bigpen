from django.urls import path

from .views import HomePage, robots_txt

urlpatterns = [
    path("robots.txt", robots_txt, name="robots_txt"),
    path("", HomePage, name="homepage"),
]
