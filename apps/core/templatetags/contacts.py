from django import template
from django.utils.html import format_html

from ..models import ContactAddress, ContactEmail, ContactNumber, ContactSocialLink

register = template.Library()


# ============================================================================
# SOCIAL MEDIA TEMPLATE TAGS
# ============================================================================


@register.simple_tag
def get_social_links():
    """
    Returns all active social media links ordered by their display order.

    Usage: {% get_social_links as social_links %}
    """
    return ContactSocialLink.objects.filter(is_active=True)


# ============================================================================
# PHONE NUMBER TEMPLATE TAGS
# ============================================================================


@register.simple_tag
def get_phone_numbers():
    """
    Returns all active phone numbers ordered by their display order.

    Usage: {% get_phone_numbers as phone_numbers %}
    """
    return ContactNumber.objects.filter(is_active=True)


@register.simple_tag
def primary_phone():
    """
    Returns the primary phone number object, or None if no primary is set.

    Usage: {% primary_phone as main_phone %}
    """
    try:
        return ContactNumber.objects.get(is_primary=True, is_active=True)
    except ContactNumber.DoesNotExist:
        return None


@register.simple_tag
def whatsapp_phone():
    """
    Returns the WhatsApp phone number object, or None if none is set.

    Usage: {% whatsapp_phone as whatsapp %}
    """
    try:
        return ContactNumber.objects.get(use_for_whatsapp=True, is_active=True)
    except ContactNumber.DoesNotExist:
        return None


# ============================================================================
# EMAIL ADDRESS TEMPLATE TAGS
# ============================================================================


@register.simple_tag
def get_email_addresses():
    """
    Returns all active email addresses ordered by their display order.

    Usage: {% get_email_addresses as email_addresses %}
    """
    return ContactEmail.objects.filter(is_active=True)


@register.simple_tag
def primary_email():
    """
    Returns the primary email address object, or None if no primary is set.

    Usage: {% primary_email as main_email %}
    """
    try:
        return ContactEmail.objects.get(is_primary=True, is_active=True)
    except ContactEmail.DoesNotExist:
        return None


@register.simple_tag
def email_link_html(email_obj, css_classes="", subject="", body=""):
    """
    Returns HTML mailto link for an email address.

    Usage: {% email_link_html email_obj "btn btn-primary" "Contact Us" "Hello!" %}
    """
    if not email_obj:
        return ""

    mailto_url = email_obj.mailto_link
    if subject or body:
        params = []
        if subject:
            params.append(f"subject={subject}")
        if body:
            params.append(f"body={body}")
        mailto_url += "?" + "&".join(params)

    return format_html(
        '<a href="{}" class="{}">{}</a>', mailto_url, css_classes, email_obj.email
    )


# ============================================================================
# PHYSICAL ADDRESS TEMPLATE TAGS
# ============================================================================


@register.simple_tag
def get_physical_addresses():
    """
    Returns all active physical addresses ordered by their display order.

    Usage: {% get_physical_addresses as addresses %}
    """
    return ContactAddress.objects.filter(is_active=True)


@register.simple_tag
def contact_form_address():
    """
    Returns the address marked for contact form use, or None if none is set.

    Usage: {% contact_form_address as main_address %}
    """
    try:
        return ContactAddress.objects.get(use_in_contact_form=True, is_active=True)
    except ContactAddress.DoesNotExist:
        return None


@register.simple_tag
def address_map_embed(address_obj, width="100%", height="270"):
    """
    Returns HTML iframe for embedded map if the address has a map_embed_url.

    Usage: {% address_map_embed address_obj "100%" "270" %}
    """
    if not address_obj or not address_obj.map_embed_url:
        return ""

    return format_html(
        '<iframe style="border:0; width: {}; height: {}px" src="{}" frameborder="0" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>',
        width,
        height,
        address_obj.map_embed_url,
    )


@register.simple_tag
def google_maps_link_html(address_obj, text="View on Google Maps", css_classes=""):
    """
    Returns HTML link to Google Maps for the address.

    Usage: {% google_maps_link_html address_obj "Get Directions" "btn btn-outline-primary" %}
    """
    if not address_obj:
        return ""

    return format_html(
        '<a href="{}" class="{}" target="_blank" rel="noopener noreferrer">{}</a>',
        address_obj.google_maps_url,
        css_classes,
        text,
    )


# ============================================================================
# UTILITY TEMPLATE TAGS
# ============================================================================


@register.simple_tag
def get_contact_info():
    """
    Returns a dictionary with all contact information for easy access.

    Usage: {% get_contact_info as contact %}
    """
    return {
        "social_links": ContactSocialLink.objects.filter(is_active=True),
        "phone_numbers": ContactNumber.objects.filter(is_active=True),
        "email_addresses": ContactEmail.objects.filter(is_active=True),
        "physical_addresses": ContactAddress.objects.filter(is_active=True),
        "primary_phone": primary_phone(),
        "whatsapp_phone": whatsapp_phone(),
        "primary_email": primary_email(),
        "contact_form_address": contact_form_address(),
    }
