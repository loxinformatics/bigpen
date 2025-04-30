from django.contrib.auth import get_user_model


def provider(request):
    return {
        "team_exists": get_user_model()
        .objects.filter(is_staff=True, is_superuser=False)
        .exists(),
    }
