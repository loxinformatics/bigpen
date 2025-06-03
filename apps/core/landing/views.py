from django.shortcuts import render


def index_page(request):
    """
    Render the landing page.
    """
    extra_context = {
        "page_title": "Welcome",
        "widget_header_breadcrumbs": False,
        # "is_header_fixed": True,
    }

    return render(request, "landing/index.html", extra_context)
