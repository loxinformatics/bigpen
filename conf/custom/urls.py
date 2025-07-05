from django.urls import include, path

urlpatterns = [
    path("", include("conf.urls")),
    path("", include("apps.ecommerce.urls")),
]
