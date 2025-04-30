# from .forms import NewsletterForm
from .models import Company


def provider(request):
    coreprovider = Company.objects.first()

    has_any_social_media_link = coreprovider and (
        coreprovider.twitter
        or coreprovider.facebook
        or coreprovider.instagram
        or coreprovider.linkedin
        or coreprovider.tiktok
        or coreprovider.youtube
        or coreprovider.whatsapp
        or coreprovider.telegram
        or coreprovider.snapchat
        or coreprovider.pinterest
    )

    footer_nav_column_1 = {
        "heading": "Useful Links",
        "navlinks": [
            {"href": "/", "label": "Home"},
            {"href": "/shop", "label": "Shop"},
            {"href": "/blog", "label": "Blog"},
            {"href": "#", "label": "Others to be added"},
            # {"href": "/admin", "label": ""},
        ],
    }

    footer_nav_column_2 = {
        "heading": "Our Services",
        "navlinks": [
            {"href": "#", "label": "To be added"},
            # {"href": "#", "label": "School Management System"},
            # {"href": "#", "label": "Online Tutorial Classes"},
            # {"href": "#", "label": "Food Supplies"},
        ],
    }

    return {
        "coreprovider": coreprovider,
        "has_any_social_media_link": bool(has_any_social_media_link),
        "footer_nav_column_1": footer_nav_column_1,
        "footer_nav_column_2": footer_nav_column_2,
        # "newsletterform": NewsletterForm(),
    }
