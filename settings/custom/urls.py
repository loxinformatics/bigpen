from django.urls import include, path

urlpatterns = [
    path("", include("settings.core.urls")),
    path("", include("apps.custom.urls")),
]
