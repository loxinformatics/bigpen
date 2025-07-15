from django.db import models

from .articles import Article


class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, help_text="Related Article"
    )
    date_created = models.DateTimeField(
        auto_now_add=True, help_text="Date Created (auto-filled)"
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Parent Comment (Optional)",
    )
    name = models.CharField(max_length=255, help_text="Your name*")
    email = models.EmailField(help_text="Your email*")
    website = models.URLField(help_text="Your website (Optional)", blank=True)
    content = models.TextField(help_text="Your Comment*")
