from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    image = models.ImageField(
        upload_to="accounts/users",
        help_text="Upload a profile pic. Preferably 600x600",
        blank=True,
    )
    position = models.CharField(
        max_length=255,
        help_text="Enter the position of the team member holds in the company",
        blank=True,
    )
    description = models.TextField(
        help_text="Give a description of the team member",
        blank=True,
    )
    facebook = models.CharField(
        max_length=255,
        help_text="Enter the facebook url",
        blank=True,
    )
    twitter = models.CharField(
        max_length=255,
        help_text="Enter the twitter url",
        blank=True,
    )
    instagram = models.CharField(
        max_length=255,
        help_text="Enter the instagram url",
        blank=True,
    )
    linkedin = models.CharField(
        max_length=255,
        help_text="Enter the linkedin url",
        blank=True,
    )

    def __str__(self):
        return self.username
