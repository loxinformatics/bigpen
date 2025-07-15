from django.urls import path

from .views.blog import blog, details

urlpatterns = [
    path("", blog, name="blogpage"),
    path("<int:pk>/", details, name="blog-details"),
]
