from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag("core/partials/vendor_bootstrap.html")
def vendor_bootstrap():
    if not settings.DEBUG:
        # Use CDN in production
        context = {
            "use_cdn": True,
            "js_url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/js/bootstrap.bundle.min.js",
            "js_integrity": "sha384-j1CDi7MgGQ12Z7Qab0qlWQ/Qqz24Gc6BM0thvEMVjHnfYGF0rmFCozFSxQBxwHKO",
        }
    else:
        # Use local files in development
        context = {
            "use_cdn": False,
            "js_url": static(
                "core/vendor/node_modules/bootstrap/dist/js/bootstrap.bundle.min.js"
            ),
        }

    return context


@register.simple_tag
def vendor_bootstrap_icons():
    if not settings.DEBUG:
        # Use CDN in production
        html = """
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/bootstrap-icons.min.css">
        """
    else:
        # Use local files in development
        html = f"""
        <link rel="stylesheet" href="{static("core/vendor/node_modules/bootstrap-icons/font/bootstrap-icons.min.css")}"/>
        """

    return mark_safe(html.strip())


@register.simple_tag
def vendor_aos():
    if not settings.DEBUG:
        # Use CDN in production
        html = """
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.min.css">
        <script defer src="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.min.js"></script>
        """
    else:
        # Use local files in development
        html = f"""
        <link rel="stylesheet" href="{static("core/vendor/node_modules/aos/dist/aos.css")}"/>
        <script defer src="{static("core/vendor/node_modules/aos/dist/aos.js")}"></script>
        """

    html += f"""
    <link rel="stylesheet" href="{static("core/init/aos/init.css")}"/>
    <script defer src="{static("core/init/aos/init.js")}"></script>
    """

    return mark_safe(html.strip())


@register.simple_tag
def vendor_waypoints():
    if not settings.DEBUG:
        # Use CDN in production
        html = """
        <script defer src="https://cdn.jsdelivr.net/npm/waypoints@4.0.1/lib/noframework.waypoints.min.js"></script>
        """
    else:
        # Use local files in development
        html = f"""
        <script defer src="{static("core/vendor/node_modules/waypoints/lib/noframework.waypoints.min.js")}"></script>
        """

    return mark_safe(html.strip())


@register.simple_tag
def vendor_isotope_layout():
    if not settings.DEBUG:
        # Use CDN in production
        html = """
        <script defer src="https://cdn.jsdelivr.net/npm/isotope-layout@3.0.6/dist/isotope.pkgd.min.js"></script>
        """
    else:
        # Use local files in development
        html = f"""
        <script defer src="{static("core/vendor/node_modules/isotope-layout/dist/isotope.pkgd.min.js")}"></script>
        """

    html += f"""
    <script defer src="{static("core/init/isotope-layout/init.js")}"></script>
    """

    return mark_safe(html.strip())


@register.simple_tag
def vendor_imagesloaded():
    if not settings.DEBUG:
        # Use CDN in production
        html = """
        <script defer src="https://cdn.jsdelivr.net/npm/imagesloaded@5.0.0/imagesloaded.pkgd.min.js"></script>
        """
    else:
        # Use local files in development
        html = f"""
        <script defer src="{static("core/vendor/node_modules/imagesloaded/imagesloaded.pkgd.min.js")}"></script>
        """

    return mark_safe(html.strip())


@register.simple_tag
def vendor_glightbox():
    if not settings.DEBUG:
        # Use CDN in production
        html = """
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/glightbox@3.3.1/dist/css/glightbox.min.css">
        <script defer src="https://cdn.jsdelivr.net/npm/glightbox@3.3.1/dist/js/glightbox.min.js"></script>
        """
    else:
        # Use local files in development
        html = f"""
        <link rel="stylesheet" href="{static("core/vendor/node_modules/glightbox/dist/css/glightbox.min.css")}"/>
        <script defer src="{static("core/vendor/node_modules/glightbox/dist/js/glightbox.min.js")}"></script>
        """

    html += f"""
    <script defer src="{static("core/init/glightbox/init.js")}"></script>
    """

    return mark_safe(html.strip())
