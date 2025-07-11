from django.views.generic import TemplateView


# Landing Page
class LandingView(TemplateView):
    template_name = "ecommerce/index.html"
    extra_context = {
        # hero section
        "show_hero": True,
        "hero_btn_1_name": "Shop Online Now",
        "hero_btn_1_url": "/#portfolio",
        # cta section
        "show_cta": True,
    }


class PortfolioView(TemplateView):
    template_name = "ecommerce/index.html"
    extra_context = {
        # portfolio section
        "show_portfolio": True,
        "portfolio_title_heading": "Our Products",
        "portfolio_title_paragraph": "Explore our curated collection of educational materials, school supplies, and academic resources designed to support learning and administration in every classroom. Quality, affordability, and purpose in every item.",
    }


# Features Page
class FeaturesView(TemplateView):
    template_name = "ecommerce/index.html"
    extra_context = {
        # features section
        "show_features": True,
        "features_title_paragraph": "What we offer",
    }


# Contact Page
class ContactView(TemplateView):
    template_name = "ecommerce/index.html"
    extra_context = {
        # contact section
        "show_contact": True,
    }
