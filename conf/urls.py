from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("core/", include("apps.core.urls")),
    path("", include("apps.home.urls")),
]

if settings.CUSTOM_APP_NAME:
    urlpatterns += [
        path(
            settings.CUSTOM_APP_URL.strip("/") + "/",
            include(f"{settings.CUSTOM_APP_NAME}.urls"),
        ),
    ]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
        *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
