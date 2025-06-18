# from django.shortcuts import redirect
from django.views.generic import TemplateView


class LandingView(TemplateView):
    """
    Render the public landing page with hero section and minimal header navigation.
    Only accessible to unauthenticated users.
    """

    template_name = "home/index.html"
    extra_context = {
        "show_hero": True,
        "hero_btn_1_name": "Dashboard",
        "hero_btn_1_login_required": True,
        "show_portfolio": True,
        "portfolio_title_heading": "Our Products",
        "portfolio_title_paragraph": "Explore our curated collection of educational materials, school supplies, and academic resources designed to support learning and administration in every classroom. Quality, affordability, and purpose in every item.",
        "show_contact": True,
    }
