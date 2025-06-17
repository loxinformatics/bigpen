from django.shortcuts import render


def landing(request):
    """
    Render the public landing page with hero section and minimal header navigation.
    """
    extra_context = {
        "show_hero": True,
        "hero_btn_1_name": "Dashboard",
        "hero_btn_1_login_required": True,
        "show_contact": True,
        "overlay_whatsapp_call_us":True,
    }

    return render(request, "home/index.html", extra_context)
