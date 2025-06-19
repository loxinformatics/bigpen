from .models import Article


def provider(request):
    return {
        "blog_exists": Article.objects.exists(),
    }
