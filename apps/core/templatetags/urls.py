import logging

from django import template
from django.core.exceptions import ImproperlyConfigured

from ..config.urls import landing_url_config

logger = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag
def landing_url():
    """
    Template tag to get the registered landing URL.

    Usage:
        {% load urls %}
        <a href="{% landing_url %}">Home</a>
    """
    try:
        return landing_url_config.get_landing_url()
    except ImproperlyConfigured:
        logger.warning("No landing URL registered")
        return ""


@register.simple_tag
def landing_url_name():
    """
    Template tag to get the registered landing URL name.

    Usage:
        {% load urls %}
        <a href="{% url landing_url_name %}">Home</a>
    """
    try:
        return landing_url_config.get_landing_url_name()
    except (ImproperlyConfigured, AttributeError):
        logger.warning("No landing URL name registered")
        return ""


@register.simple_tag
def landing_url_with_fragment(fragment=None):
    """
    Template tag to get the landing URL with an optional fragment.

    Usage:
        {% load urls %}
        <a href="{% landing_url_with_fragment 'hero' %}">Home</a>
        <a href="{% landing_url_with_fragment %}">Home</a>
    """
    try:
        base_url = landing_url_config.get_landing_url()
    except ImproperlyConfigured:
        logger.warning("No landing URL registered")
        base_url = ""

    if fragment:
        return f"{base_url}#{fragment}"
    return base_url


@register.filter
def is_landing_url(url_name):
    """
    Filter to check if a given URL name is the registered landing URL.

    Usage:
        {% load urls %}
        {% if 'landing'|is_landing_url %}
            <span class="active">Current Home</span>
        {% endif %}
    """
    try:
        registered_name = landing_url_config.get_landing_url_name()
        return url_name == registered_name
    except (ImproperlyConfigured, AttributeError):
        return False


@register.simple_tag(takes_context=True)
def is_landing_page(context):
    """
    Template tag to check if the current page is the landing page.

    Usage:
        {% load urls %}
        {% is_landing_page as is_landing %}
        {% if is_landing %}
            <div class="landing-banner">Welcome to our landing page!</div>
        {% endif %}
    """
    request = context.get("request")
    if not request or not landing_url_config:
        return False

    try:
        landing_url = landing_url_config.get_landing_url()
        current_path = request.path
        return current_path == landing_url
    except (ImproperlyConfigured, AttributeError):
        return False


@register.simple_tag
def portal_url():
    """
    Return the portal URL path.
    Usage: {% portal_url %}
    """
    return "core/portal/"
