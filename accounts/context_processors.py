from accounts.models import CustomUser


def accounts(request):
    return {
        "team_exists": CustomUser.objects.filter(is_staff=True, is_superuser=False).exists(),
    }
