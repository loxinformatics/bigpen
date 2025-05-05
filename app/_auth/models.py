from django.contrib.auth.models import AbstractUser, Group
from django.core.exceptions import ValidationError
from django.db import models

from .apps import PROTECTED_GROUPS


class UserGroup(Group):
    class Meta:
        proxy = True
        verbose_name = "User group"
        verbose_name_plural = "User groups"

    def is_protected(self):
        return self.name in PROTECTED_GROUPS.values()

    def is_default_group(self):
        return self.is_protected()

    is_default_group.boolean = True  # Shows icon in admin
    is_default_group.short_description = "Default Group"  # Column header in admin

    def clean(self):
        super().clean()
        if not self.pk:  # Only for new groups
            if UserGroup.objects.filter(name=self.name).exists():
                raise ValidationError(
                    f"A group with name '{self.name}' already exists."
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class User(AbstractUser):
    # Add back the email field, make it optional
    email = models.EmailField(
        "email address",
        blank=True,
        null=True,
        unique=False,
        help_text="Optional. Used for notifications and password reset.",
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    # Name field that automatically combines first_name and last_name
    @property
    def name(self):
        """Full name (first and last name combined, read-only)."""
        return f"{self.first_name} {self.last_name}".strip()

    # profile
    image = models.ImageField(
        upload_to="images/users/",
        help_text="Upload a profile image (recommended size: 600x600). [Optional]",
        blank=True,
        null=True,
        verbose_name="Profile image",
    )
    title = models.CharField(
        max_length=100,
        blank=True,
        help_text="Enter your professional title or role. [Optional]",
    )
    description = models.TextField(
        blank=True, help_text="Add a short bio or description. [Optional]"
    )

    # Socials
    twitter_x = models.URLField(
        blank=True, help_text="Link to your Twitter/X profile. [Optional]"
    )
    facebook = models.URLField(
        blank=True, help_text="Link to your Facebook profile. [Optional]"
    )
    instagram = models.URLField(
        blank=True, help_text="Link to your Instagram profile. [Optional]"
    )
    linkedin = models.URLField(
        blank=True, help_text="Link to your LinkedIn profile. [Optional]"
    )
    github = models.URLField(
        blank=True, help_text="Link to your GitHub profile. [Optional]"
    )
    youtube = models.URLField(
        blank=True, help_text="Link to your YouTube channel. [Optional]"
    )
    website = models.URLField(
        blank=True,
        help_text="Link to your personal or professional website. [Optional]",
    )

    def __str__(self):
        return f"{self.name}"
