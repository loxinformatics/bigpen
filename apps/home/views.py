# from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.management.mixins import AnonymousRequiredMixin


class LandingView(AnonymousRequiredMixin, TemplateView):
    """
    Render the public landing page with hero section and minimal header navigation.
    Only accessible to unauthenticated users.
    """

    template_name = "home/index.html"
    extra_context = {
        "show_hero": True,
        "hero_btn_1_name": "Dashboard",
        "hero_btn_1_login_required": True,
        "show_contact": True,
    }
