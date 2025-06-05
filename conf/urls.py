from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # django and third-party
    path("admin/", admin.site.urls),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    # core
    path("auth/", include("apps.core.authentication.urls")),
    path("", include("apps.core.landing.urls")),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
