from django.conf import settings
from django.core.cache import cache

from .models import BaseDetail, BaseImage


def load_base_config():
    """Fetch BaseDetail and BaseImage data from the database."""
    config = {
        **{f"{d.name}": d.value for d in BaseDetail.objects.only("name", "value")},
        **{i.name.lower(): i.image.url for i in BaseImage.objects.all() if i.image},
    }
    return config


def get_base_detail(name, default=""):
    """Return base config, using cache in production, always fresh in DEBUG."""
    if settings.DEBUG:
        return load_base_config().get(name, default)

    base_config = cache.get("base_config")
    if base_config is None:
        base_config = load_base_config()
        cache.set("base_config", base_config, 3600)

    return base_config.get(name, default)
