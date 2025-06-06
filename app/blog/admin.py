from django.contrib import admin

from .forms import ArticleForm
from .models import Article, Category, Tag


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm


admin.site.register(Category)
admin.site.register(Tag)
