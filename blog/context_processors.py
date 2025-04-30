from .models import Article


def blogprovider(request):
    return {
        "blog_exists": Article.objects.exists(),
    }
