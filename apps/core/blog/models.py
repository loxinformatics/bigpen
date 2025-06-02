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
    )
    image = models.ImageField(upload_to="blog/articles/", help_text="Article Image")
    title = models.CharField(max_length=255, help_text="Article Title")
    content = models.TextField(help_text="Article Content (Optional)", blank=True)

    def __str__(self):
        return self.title


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
