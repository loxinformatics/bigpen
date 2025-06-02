from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Organization(models.Model):
    """
    Generic model for representing various types of organizations:
    companies, schools, churches, ecommerce stores, NGOs, etc.
    """

    class Meta:
        verbose_name = "App organization settings"
        verbose_name_plural = "App organization settings"

    # Contact Info
    website = models.URLField(
        help_text="Main website URL of your company, including https://."
    )
    primary_phone = PhoneNumberField(
        region="KE", help_text="Main business phone number (e.g., +254712345678)."
    )
    secondary_phone = PhoneNumberField(
        region="KE", blank=True, help_text="Alternate contact number (optional)."
    )
    other_phone = PhoneNumberField(
        region="KE", blank=True, help_text="Any other backup phone number (optional)."
    )
    primary_email = models.EmailField(
        help_text="Primary business email address for customer or partner contact."
    )
    secondary_email = models.EmailField(
        blank=True, help_text="Alternate email address (optional)."
    )
    other_email = models.EmailField(
        blank=True, help_text="Any other backup email (optional)."
    )

    # Addressing Info
    building = models.CharField(
        max_length=255,
        blank=True,
        help_text="Name or number of the building where the company is located (optional).",
    )
    street = models.CharField(
        max_length=255,
        blank=True,
        help_text="Street or road name for the company address (optional).",
    )
    PO_box = models.CharField(
        max_length=255,
        blank=True,
        help_text="Postal Box address (e.g., P.O. Box 1234) (optional).",
    )
    city_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="City or town name where the company is based (optional).",
    )
    zip_code = models.CharField(
        max_length=255,
        blank=True,
        help_text="Postal/ZIP code for your address (optional).",
    )
    map_url = models.TextField(
        blank=True,
        help_text="Google Maps embed URL for your location (Format: https://www.google.com/maps/embed?pb=...) (optional).",
    )

    # Social Media
    twitter = models.URLField(
        blank=True, help_text="Link to your official Twitter/X account (optional)."
    )
    facebook = models.URLField(
        blank=True, help_text="Link to your official Facebook page (optional)."
    )
    instagram = models.URLField(
        blank=True, help_text="Link to your Instagram profile (optional)."
    )
    linkedin = models.URLField(
        blank=True, help_text="Link to your company's LinkedIn page (optional)."
    )
    tiktok = models.URLField(
        blank=True, help_text="Link to your business TikTok profile (optional)."
    )
    youtube = models.URLField(
        blank=True, help_text="Link to your YouTube channel (optional)."
    )
    whatsapp = models.URLField(
        blank=True,
        help_text="WhatsApp Business contact link (Format: https://wa.me/{phone_number}, e.g., https://wa.me/254712345678) (optional).",
    )
    telegram = models.URLField(
        blank=True, help_text="Telegram channel or group link (optional)."
    )
    snapchat = models.URLField(
        blank=True, help_text="Link to your Snapchat profile (optional)."
    )
    pinterest = models.URLField(
        blank=True, help_text="Link to your Pinterest board or profile (optional)."
    )

    def clean(self):
        if Organization.objects.exists() and not self.pk:
            raise ValidationError("There can be only one Organization instance.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return "Organization Settings"


class ListCategory(models.Model):
    class Meta:
        verbose_name_plural = "List categories"

    name = models.CharField(
        max_length=255,
        help_text="Category name that groups related list items (e.g., 'Electronics', 'Furniture').",
    )

    def __str__(self):
        return self.name


class ListItem(models.Model):
    class Meta:
        ordering = ("name",)

    category = models.ForeignKey(
        ListCategory,
        on_delete=models.CASCADE,
        related_name="items",
    )
    name = models.CharField(
        max_length=255,
        help_text="Name of the item.",
    )
    # image = models.ImageField(
    #     upload_to="list_items/",
    #     blank=True,
    #     null=True,
    #     help_text="Upload an image representing this item (optional).",
    # )
    bootstrap_icon = models.CharField(
        max_length=255,
        blank=True,
        help_text="Bootstrap icon class for this item (optional). Example: 'bi bi-cart' for a shopping cart icon. Find icons at [Bootstrap Icons](https://icons.getbootstrap.com/).",
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of this item, including features or specifications (optional).",
    )

    def __str__(self):
        return self.name
