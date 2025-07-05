from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("core/", include("apps.core.urls")),
    path("blog/", include("apps.blog.urls")),
    path("", include(f"{settings.SITE_APP}.urls")),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
        *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
