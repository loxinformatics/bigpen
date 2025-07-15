from django.conf import settings
from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=100, help_text="Category Name")

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, help_text="Tag Name")

    def __str__(self):
        return self.name


class Article(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        help_text="Article Category (Optional)",
    )
    tags = models.ManyToManyField(Tag, blank=True, help_text="Tags (Optional)")
    date_created = models.DateTimeField(
        auto_now_add=True, help_text="Date Created (auto-filled)"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_articles",
        help_text="Article Author",
        null=True,  # Allow null values temporarily
        blank=True,  # Allow blank in forms
    )
    image = models.ImageField(upload_to="blog/articles/", help_text="Article Image")
    title = models.CharField(max_length=255, help_text="Article Title")
    content = models.TextField(help_text="Article Content (Optional)", blank=True)

    def save(self, *args, **kwargs):
        # Get the current user from kwargs if provided (for programmatic saves)
        user = kwargs.pop("user", None)

        # For admin panel, get the user from request if available
        request = kwargs.pop("request", None)

        # Set author only if it's not already set
        if not self.author_id:
            if user:
                self.author = user
            elif request and hasattr(request, "user") and request.user.is_authenticated:
                self.author = request.user

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
