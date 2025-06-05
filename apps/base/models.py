from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class OrgDetail(models.Model):
    ORG_DETAIL_CHOICES = [
        ("org_name", "Organization Name"),
        ("org_description", "Organization Description"),
        ("org_url", "Organization URL"),
        ("org_theme_color", "Organization Theme Color"),
    ]

    name = models.CharField(max_length=25, choices=ORG_DETAIL_CHOICES, unique=True)

    value = models.CharField(
        max_length=255,
        help_text="Value for the organization detail (e.g., name, description, etc.)",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Organization Detail"
        verbose_name_plural = "Organization Details"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_name_display()} - {self.value}"

    @property
    def display_name(self):
        """Returns the human-readable name of the organization detail"""
        return self.get_name_display()


class OrgGraphic(models.Model):
    ORG_GRAPHIC_CHOICES = [
        ("org_logo", "Logo"),
        ("org_favicon", "Favicon"),
        ("org_apple_touch_icon", "Apple Touch Icon"),
        ("org_cover_image", "Cover / Hero image"),
    ]

    name = models.CharField(max_length=25, choices=ORG_GRAPHIC_CHOICES, unique=True)

    image = models.ImageField(
        upload_to="base/site",
        help_text="Image file for logos, favicons, etc.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Organization Graphic"
        verbose_name_plural = "Organization Graphics"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_name_display()}"

    @property
    def display_name(self):
        """Returns the human-readable name of the organization graphic"""
        return self.get_name_display()


class SocialMediaLink(models.Model):
    # Social media platform choices with their corresponding Bootstrap icons
    SOCIAL_MEDIA_CHOICES = [
        ("facebook", "Facebook"),
        ("twitter", "X (formerly Twitter)"),
        ("instagram", "Instagram"),
        ("linkedin", "LinkedIn"),
        ("youtube", "YouTube"),
        ("tiktok", "TikTok"),
        ("pinterest", "Pinterest"),
        ("snapchat", "Snapchat"),
        ("discord", "Discord"),
        ("telegram", "Telegram"),
        ("github", "GitHub"),
        ("reddit", "Reddit"),
        ("twitch", "Twitch"),
    ]

    # Bootstrap icon mapping
    ICON_MAPPING = {
        "facebook": "bi bi-facebook",
        "twitter": "bi bi-twitter-x",
        "instagram": "bi bi-instagram",
        "linkedin": "bi bi-linkedin",
        "youtube": "bi bi-youtube",
        "tiktok": "bi bi-tiktok",
        "pinterest": "bi bi-pinterest",
        "snapchat": "bi bi-snapchat",
        "discord": "bi bi-discord",
        "telegram": "bi bi-telegram",
        "github": "bi bi-github",
        "reddit": "bi bi-reddit",
        "twitch": "bi bi-twitch",
    }

    name = models.CharField(max_length=20, choices=SOCIAL_MEDIA_CHOICES, unique=True)

    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Bootstrap icon class (auto-populated based on name)",
    )

    url = models.URLField(help_text="URL to your selected social media profile")

    is_active = models.BooleanField(
        default=True, help_text="Whether this social media link should be displayed"
    )

    order = models.PositiveIntegerField(
        default=0, help_text="Display order (lower numbers appear first)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Social Media Link"
        verbose_name_plural = "Social Media Links"

    def save(self, *args, **kwargs):
        # Automatically set the icon based on the selected name
        if self.name in self.ICON_MAPPING:
            self.icon = self.ICON_MAPPING[self.name]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_name_display()} - {self.url}"

    @property
    def display_name(self):
        """Returns the human-readable name of the social media platform"""
        return self.get_name_display()

    @property
    def icon_html(self):
        """Returns HTML for the Bootstrap icon"""
        return f'<i class="{self.icon}"></i>' if self.icon else ""


class PhoneNumber(models.Model):
    number = PhoneNumberField(
        region="KE",  # Default to Kenya, but accepts international numbers
        help_text="Phone number (e.g., +254712345678 or 0712345678)",
        unique=True,  # Add unique constraint
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Whether this phone number should be displayed",
    )

    is_primary = models.BooleanField(
        default=False,
        help_text="Mark as primary phone number. If is_active is False, this will be ignored.",
    )

    use_for_whatsapp = models.BooleanField(
        default=False,
        help_text="Whether this phone number should be used for WhatsApp. If is_active is False, this will be ignored.",
    )

    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "number"]
        verbose_name = "Phone Number"
        verbose_name_plural = "Phone Numbers"

    def save(self, *args, **kwargs):
        # If number is not active, ensure it's not primary or WhatsApp
        if not self.is_active:
            self.is_primary = False
            self.use_for_whatsapp = False

        # Ensure only one primary phone number exists
        if self.is_primary:
            PhoneNumber.objects.filter(is_primary=True).exclude(pk=self.pk).update(
                is_primary=False
            )

        # Ensure only one WhatsApp number exists
        if self.use_for_whatsapp:
            PhoneNumber.objects.filter(use_for_whatsapp=True).exclude(
                pk=self.pk
            ).update(use_for_whatsapp=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.international_format

    @property
    def formatted_number(self):
        """Returns the formatted phone number"""
        return str(self.number)

    @property
    def national_format(self):
        """Returns phone number in national format"""
        return self.number.as_national if self.number else ""

    @property
    def international_format(self):
        """Returns phone number in international format"""
        return self.number.as_international if self.number else ""

    @property
    def tel_link(self):
        """Returns a tel: link for the phone number"""
        return f"tel:{self.number}"

    @property
    def whatsapp_link(self):
        """Returns a WhatsApp link for the phone number"""
        if self.use_for_whatsapp and self.number:
            # Remove the '+' and any spaces for WhatsApp URL
            clean_number = str(self.number).replace("+", "").replace(" ", "")
            return f"https://wa.me/{clean_number}"
        return ""


class EmailAddress(models.Model):
    email = models.EmailField(
        help_text="Email address (e.g., user@example.com)",
        unique=True,  # Add unique constraint
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Whether this email address should be displayed",
    )

    is_primary = models.BooleanField(
        default=False,
        help_text="Mark as primary email address. If is_active is False, this will be ignored.",
    )

    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "email"]
        verbose_name = "Email Address"
        verbose_name_plural = "Email Addresses"

    def save(self, *args, **kwargs):
        # If email is not active, ensure it's not primary
        if not self.is_active:
            self.is_primary = False

        # Ensure only one primary email address exists
        if self.is_primary:
            EmailAddress.objects.filter(is_primary=True).exclude(pk=self.pk).update(
                is_primary=False
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    @property
    def mailto_link(self):
        """Returns a mailto: link for the email address"""
        return f"mailto:{self.email}"


class PhysicalAddress(models.Model):
    label = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional custom label for this address",
        unique=True,  # Ensure labels are unique
        # This can be useful for distinguishing between multiple addresses
    )

    building = models.CharField(
        max_length=100,
        blank=True,
        help_text="Building name or number (e.g., Britam Tower, Block A)",
    )

    street_address = models.CharField(
        max_length=255,
        help_text="Street address including house number and street name",
    )

    city = models.CharField(
        max_length=100,
        help_text="City name",
    )

    state_province = models.CharField(
        max_length=100,
        blank=True,
        help_text="State, province, or county (e.g., Vihiga County)",
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True,
        help_text="ZIP code, postal code, or equivalent",
    )

    country = models.CharField(
        max_length=100,
        default="Kenya",
        help_text="Country name",
    )

    map_embed_url = models.URLField(
        blank=True,
        help_text="Google Maps/Other map provider embed URL for displaying in iframes (e.g., https://www.google.com/maps/embed?pb=...)",
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Whether this address should be displayed",
    )

    is_primary = models.BooleanField(
        default=False,
        help_text="Mark as primary address which is used for contact forms and maps. If is_active is False, this will be ignored.",
    )

    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "label", "city"]
        verbose_name = "Physical Address"
        verbose_name_plural = "Physical Addresses"

    def save(self, *args, **kwargs):
        # If address is not active, ensure it's not primary
        if not self.is_active:
            self.is_primary = False

        # Ensure only one primary address exists
        if self.is_primary:
            PhysicalAddress.objects.filter(is_primary=True).exclude(pk=self.pk).update(
                is_primary=False
            )

        super().save(*args, **kwargs)

    def __str__(self):
        if self.label:
            return self.label
        return self.city

    @property
    def full_address(self):
        """Returns the complete formatted address"""
        address_parts = [self.street_address, self.city]

        if self.state_province:
            address_parts.append(self.state_province)

        if self.postal_code:
            address_parts.append(self.postal_code)

        address_parts.append(self.country)

        return ", ".join(address_parts)

    @property
    def short_address(self):
        """Returns a shortened version of the address"""
        return f"{self.city}, {self.country}"

    @property
    def google_maps_url(self):
        """Returns a Google Maps URL for this address"""
        import urllib.parse

        query = urllib.parse.quote_plus(self.full_address)
        return f"https://www.google.com/maps/search/?api=1&query={query}"
