from django.shortcuts import render


def index(request):
    extra_context = {
        "page_title": "Welcome",
        "header_position": "fixed",
        "header_cta_btn_url_path": "",
        "header_cta_btn_login_required": True
    }

    return render(request, "landing/index.html", extra_context)
