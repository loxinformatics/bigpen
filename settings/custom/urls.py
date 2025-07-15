from django.urls import include, path

urlpatterns = [
    path("", include("settings.urls")),
    path("", include("apps.ecommerce.urls")),
]
