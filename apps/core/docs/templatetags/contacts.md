# Contact Template Tags Usage Guide

**Load the template tags** in your Django templates:
   ```django
   {% load contacts %}
   ```

## Social Media Template Tags

```django
<!-- Get all active social media links -->
{% get_social_links as social_links %}
{% for link in social_links %}
    <a href="{{ link.url }}">{{ link.display_name }}</a>
{% endfor %}

<!-- Get icon HTML (<i></i>) for a specific platform -->
{% social_icon "facebook" %}

<!-- Get complete HTML link for a platform -->
{% social_link_html "twitter" "btn btn-primary" %}
```

## Phone Number Template Tags

```django
<!-- Get all active phone numbers -->
{% get_phone_numbers as phones %}

<!-- Get primary phone number -->
{% primary_phone as main_phone %}
{% if main_phone %}
    <p>Call us: {{ main_phone.international_format }}</p>
{% endif %}

<!-- Get WhatsApp phone number -->
{% whatsapp_phone as whatsapp %}
{% if whatsapp %}
    <a href="{{ whatsapp.whatsapp_link }}">Chat on WhatsApp</a>
{% endif %}

<!-- Generate phone link HTML -->
{% primary_phone as main_phone %}
{% phone_link_html main_phone "national" "btn btn-outline-primary" %}

<!-- Generate WhatsApp link -->
{% whatsapp_link_html whatsapp "Message us" "btn btn-success" %}
```

## Email Address Template Tags

```django
<!-- Get all active email addresses -->
{% get_email_addresses as emails %}

<!-- Get primary email address -->
{% primary_email as main_email %}
{% if main_email %}
    <p>Email: {{ main_email.email }}</p>
{% endif %}

<!-- Generate email link with subject and body -->
{% primary_email as main_email %}
{% email_link_html main_email "btn btn-primary" "Contact Us" "Hello, I would like to..." %}
```

## Physical Address Template Tags

```django
<!-- Get all active addresses -->
{% get_physical_addresses as addresses %}

<!-- Get contact form address -->
{% contact_form_address as main_address %}
{% if main_address %}
    <p>{{ main_address.full_address }}</p>
{% endif %}

<!-- Generate map embed -->
{% contact_form_address as main_address %}
{% address_map_embed main_address "100%" "400" %}

<!-- Generate Google Maps link -->
{% google_maps_link_html main_address "Get Directions" "btn btn-outline-primary" %}
```

## Complete Contact Information

```django
<!-- Get all contact information in one object -->
{% get_contact_info as contact %}

<!-- Access specific parts -->
<p>Primary Phone: {{ contact.primary_phone.international_format }}</p>
<p>Primary Email: {{ contact.primary_email.email }}</p>
<p>Main Address: {{ contact.contact_form_address.full_address }}</p>
```

## Example Usage in Templates

### Header Template

```django
{% load contacts %}

<header>
    <nav>
        <!-- Primary contact info in header -->
        {% primary_phone as main_phone %}
        {% primary_email as main_email %}
        
        {% if main_phone %}
            <span class="header-phone">
                {% phone_link_html main_phone "international" "phone-link" %}
            </span>
        {% endif %}
        
        {% if main_email %}
            <span class="header-email">
                {% email_link_html main_email "email-link" %}
            </span>
        {% endif %}
        
        <!-- WhatsApp quick access -->
        {% whatsapp_link_html None "Chat with us" "whatsapp-btn" %}
    </nav>
</header>
```

### Business Card Widget

```django
{% load contacts %}

<div class="business-card">
    <h4>Contact Information</h4>
    
    {% get_contact_info as contact %}
    
    {% if contact.primary_phone %}
        <div class="contact-item">
            <i class="bi bi-telephone"></i>
            {{ contact.primary_phone.international_format }}
        </div>
    {% endif %}
    
    {% if contact.primary_email %}
        <div class="contact-item">
            <i class="bi bi-envelope"></i>
            {{ contact.primary_email.email }}
        </div>
    {% endif %}
    
    {% if contact.contact_form_address %}
        <div class="contact-item">
            <i class="bi bi-geo-alt"></i>
            {{ contact.contact_form_address.short_address }}
        </div>
    {% endif %}
    
    {% if contact.social_links %}
        <div class="social-icons">
            {% for social in contact.social_links %}
                <a href="{{ social.url }}" target="_blank" title="{{ social.display_name }}">
                    {{ social.icon_html|safe }}
                </a>
            {% endfor %}
        </div>
    {% endif %}
</div>
```

## Notes

- All template tags respect the `is_active` field and only show active items
- Items are automatically ordered by the `order` field
- Primary/main items are automatically identified
- URLs are safely generated with proper protocols
- All external links include `rel="noopener noreferrer"` for security
- Template tags handle missing data gracefully (no errors on empty results)