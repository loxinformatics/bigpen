# from .forms import NewsletterForm
from .models import Organization
from app.shop.models import Category


def provider(request):
    org = Organization.objects.first()

    has_any_social_media_link = org and (
        org.twitter
        or org.facebook
        or org.instagram
        or org.linkedin
        or org.tiktok
        or org.youtube
        or org.whatsapp
        or org.telegram
        or org.snapchat
        or org.pinterest
    )

    footer_nav_column_1 = {
        "heading": "Useful Links",
        "navlinks": [
            {"href": "/", "label": "Home"},
            {"href": "/shop/items/", "label": "Shop"},
            {"href": "/blog", "label": "Blog"},
            # {"href": "/admin", "label": ""},
        ],
    }

    categories = Category.objects.all()
    footer_nav_column_2 = {
        "heading": "Our Products",
        "navlinks": [
            {
                "href": f"/shop/items/?category={category.name}",
                "label": category.name,
            }
            for category in categories
        ],
    }

    return {
        "company_fullname": "Online BigPen Kenya",
        "company_shortname": "BigPen",
        "company_motto": "We Deliver Stationery In less than 24 hours",
        "company_accent_color": "red",
        "org": org,
        "has_any_social_media_link": bool(has_any_social_media_link),
        "footer_nav_column_1": footer_nav_column_1,
        "footer_nav_column_2": footer_nav_column_2,
        # "newsletterform": NewsletterForm(),
    }
