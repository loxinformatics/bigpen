from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # vendor
    path("__reload__/", include("django_browser_reload.urls")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    # admin
    path("admin/", admin.site.urls),
    # custom
    path("", include("core.urls")),
    path("blog/", include("blog.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    # path("", include("home.urls")),
    # path("gallery/", include("gallery.urls")),
    # path("lessons/", include("lessons.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
