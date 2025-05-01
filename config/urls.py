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
    path("", include("app.home.urls")),
    path("_auth/", include("app._auth.urls")),
    path("blog/", include("app.blog.urls")),
    path("shop/", include("app.shop.urls")),
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Online BigPen Kenya"
admin.site.site_title = "Admin | Online BigPen Kenya"
admin.site.index_title = "Online BigPen Kenya Administration"
