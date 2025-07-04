import logging

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

logger = logging.getLogger(__name__)


class Ordering(models.Model):
    class Meta:
        abstract = True

    order = models.PositiveIntegerField(
        default=1,
        help_text="Display order (lower numbers - zero included - appear first)",
    )


class BootstrapIcon(models.Model):
    class Meta:
        abstract = True

    bootstrap_icon = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional. Bootstrap icon class or path for the item. Example: 'bi bi-cart' for a shopping cart icon. Find icons at [Bootstrap Icons](https://icons.getbootstrap.com/).",
    )


class DateFields(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Date and time created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time last updated.",
    )


# ============================================================================
# BASE MODELS
# ============================================================================

BASE_DETAIL_CHOICES = [
    ("base_name", "Full Name"),
    ("base_short_name", "Short Name"),
    ("base_description", "Motto / Description"),
    ("base_theme_color", "Theme Color"),
    ("base_url", "Website URL"),
    ("base_author", "Author's Name"),
    ("base_author_url", "Author's Website URL"),
]

BASE_IMAGE_CHOICES = [
    ("base_logo", "Logo"),
    ("base_favicon", "Favicon"),
    ("base_apple_touch_icon", "Apple touch icon"),
    ("base_hero_image", "Hero / cover image"),
]


class UniqueChoiceBaseModel(models.Model):
    """
    Abstract base model for models with a unique 'name' choice field,
    customizable display ordering, and timestamp tracking.
    """

    name = models.CharField(max_length=25, unique=True)
    ordering = models.PositiveIntegerField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    CHOICES = []  # Override in subclass
    ORDER_MAPPING = {}  # Override in subclass

    class Meta:
        abstract = True
        ordering = ["ordering"]

    def save(self, *args, **kwargs):
        """
        Assigns ordering based on ORDER_MAPPING before saving.
        Defaults to 999 if not found.
        """
        if self.name:
            self.ordering = self.ORDER_MAPPING.get(self.name, 999)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_name_display()

    @property
    def display_name(self):
        """Returns the human-readable name of the item"""
        return self.get_name_display()


class BaseDetail(UniqueChoiceBaseModel):
    """
    Represents a customizable organization text detail, such as name, motto,
    theme color, or URLs.
    """

    CHOICES = BASE_DETAIL_CHOICES
    ORDER_MAPPING = {key: i + 1 for i, (key, _) in enumerate(CHOICES)}

    name = models.CharField(max_length=25, choices=CHOICES, unique=True)
    value = models.CharField(
        max_length=255, blank=True, help_text="Value for the organization detail."
    )


class BaseImage(UniqueChoiceBaseModel):
    """
    Represents organization-related image assets like logos, favicons,
    and hero images.
    """

    CHOICES = BASE_IMAGE_CHOICES
    ORDER_MAPPING = {key: i + 1 for i, (key, _) in enumerate(CHOICES)}

    name = models.CharField(max_length=25, choices=CHOICES, unique=True)
    image = models.ImageField(
        upload_to="core/base",
        null=True,
        blank=True,
        help_text="""
            Upload images in recommended sizes: Logo (512x512), Favicon (32x32), Apple Touch Icon (180x180), Hero Image (2560x1440 or 1920x1080).
            PNG format recommended for logos and icons to preserve transparency. JPG format recommended for hero.
        """,
    )
    description = models.TextField(editable=False)

    def save(self, *args, **kwargs):
        # Set description based on the chosen 'name'
        if self.name == "base_logo":
            self.description = "The organization's main logo. Recommended size: 512x512 pixels. PNG format is recommended for transparency."
        elif self.name == "base_favicon":
            self.description = "The favicon displayed in browser tabs. Recommended size: 32x32 pixels. Should be a .ico file."
        elif self.name == "base_apple_touch_icon":
            self.description = "The icon used when users add the website to their home screen on Apple devices. Recommended size: 180x180 pixels."
        elif self.name == "base_hero_image":
            self.description = "The prominent hero or cover image for the website. Recommended sizes: 2560x1440 or 1920x1080 pixels. JPG format is recommended."
        else:
            self.description = "Custom image for the organization."

        super().save(*args, **kwargs)


# ============================================================================
# CONTACT MODELS
# ============================================================================


class Contacts(models.Model):
    is_active = models.BooleanField(
        default=True, help_text="Whether this should be displayed"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ContactSocialLink(Contacts, Ordering):
    """
    Represents a social media link with associated Bootstrap icon class,
    display status, and display order.
    """

    class Meta:
        ordering = ["order", "name"]

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

    def save(self, *args, **kwargs):
        """Auto-assign icon based on the platform name before saving."""
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
        if self.icon:
            return f'<i class="{self.icon}"></i>'
        return ""


class ContactNumber(Contacts, Ordering):
    """
    Stores phone numbers with metadata such as primary use, WhatsApp usage,
    display status, and order.
    """

    class Meta:
        ordering = ["order", "number"]

    number = PhoneNumberField(
        region="KE",
        help_text="Phone number (e.g., +254712345678 or 0712345678)",
        unique=True,
    )
    is_primary = models.BooleanField(
        default=False,
        help_text="Mark as primary phone number. If is_active is False, this will be ignored.",
    )
    use_for_whatsapp = models.BooleanField(
        default=False,
        help_text="Whether this phone number should be used for WhatsApp. If is_active is False, this will be ignored.",
    )

    def save(self, *args, **kwargs):
        """
        Enforces business rules:
        - Only one primary number allowed
        - Only one WhatsApp number allowed
        - If inactive, disables primary and WhatsApp flags
        """
        if not self.is_active:
            self.is_primary = False
            self.use_for_whatsapp = False

        if self.is_primary:
            ContactNumber.objects.filter(is_primary=True).exclude(pk=self.pk).update(
                is_primary=False
            )

        if self.use_for_whatsapp:
            ContactNumber.objects.filter(use_for_whatsapp=True).exclude(
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
            clean_number = str(self.number).replace("+", "").replace(" ", "")
            return f"https://wa.me/{clean_number}"
        return ""


class ContactEmail(Contacts, Ordering):
    """
    Stores email addresses with metadata for display, priority,
    and ordering.
    """

    class Meta:
        ordering = ["order", "email"]

    email = models.EmailField(
        help_text="Email address (e.g., user@example.com)",
        unique=True,
    )
    is_primary = models.BooleanField(
        default=False,
        help_text="Mark as email address to be used in contact forms. If is_active is False, this will be ignored.",
    )

    def save(self, *args, **kwargs):
        """
        Ensures only one email is set as primary and disables primary
        if email is not active.
        """
        if not self.is_active:
            self.is_primary = False

        if self.is_primary:
            ContactEmail.objects.filter(is_primary=True).exclude(pk=self.pk).update(
                is_primary=False
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    @property
    def mailto_link(self):
        """Returns a mailto: link for the email address"""
        return f"mailto:{self.email}"


class ContactAddress(Contacts, Ordering):
    """
    Stores physical addresses, with optional Google Maps embed URLs,
    display order, and contact form preferences.
    """

    class Meta:
        ordering = ["order", "label", "city"]
        verbose_name_plural = "Contact addresses"

    label = models.CharField(
        max_length=100,
        help_text="Custom label for this address e.g Main Office Address",
        unique=True,
    )
    building = models.CharField(
        max_length=100,
        blank=True,
        help_text="Building name or number (e.g., Britam Tower, Block A)",
    )
    street_address = models.CharField(
        max_length=255,
        help_text="Street address including house number and street name",
        blank=True,
    )
    city = models.CharField(max_length=100, help_text="City name", blank=True)
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
        max_length=100, default="Kenya", help_text="Country name", blank=True
    )
    map_embed_url = models.URLField(
        blank=True,
        max_length=500,
        help_text="Google Maps/Other map provider embed URL for displaying in iframes",
    )
    use_in_contact_form = models.BooleanField(
        default=False,
        help_text="Mark this as the address to use in contact forms and maps. Only one active address can be selected.",
    )

    def save(self, *args, **kwargs):
        """
        Ensures only one address is marked for contact form use.
        Automatically disables this flag if the address is inactive.
        """
        if not self.is_active:
            self.use_in_contact_form = False

        if self.use_in_contact_form:
            ContactAddress.objects.filter(use_in_contact_form=True).exclude(
                pk=self.pk
            ).update(use_in_contact_form=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.label if self.label else self.city

    @property
    def full_address(self):
        """Returns the full formatted address string"""
        parts = [self.street_address, self.city]
        if self.state_province:
            parts.append(self.state_province)
        if self.postal_code:
            parts.append(self.postal_code)
        parts.append(self.country)
        return ", ".join(parts)

    @property
    def short_address(self):
        """Returns a shorter city + country format"""
        return f"{self.city}, {self.country}"

    @property
    def google_maps_url(self):
        """Generates a Google Maps search URL for the full address"""
        import urllib.parse

        query = urllib.parse.quote_plus(self.full_address)
        return f"https://www.google.com/maps/search/?api=1&query={query}"


# ============================================================================
# LIST MODELS
# ============================================================================


class ListCategory(Ordering, BootstrapIcon, DateFields):
    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "List categories"

    name = models.CharField(
        max_length=255,
        help_text="Category name that groups related list items (e.g., 'Electronics', 'Furniture').",
    )

    def __str__(self):
        return self.name


class ListItem(Ordering, BootstrapIcon, DateFields):
    class Meta:
        ordering = ["order", "name"]

    category = models.ForeignKey(
        ListCategory,
        on_delete=models.CASCADE,
        related_name="items",
    )
    name = models.CharField(
        max_length=255,
        help_text="Name of the item.",
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of this item, including features or specifications (optional).",
    )

    def __str__(self):
        return self.name
