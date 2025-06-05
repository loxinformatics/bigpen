from django.contrib import admin
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import OrgDetail


def set_admin_site_titles():
    # Fetch OrgDetail values
    org_name = OrgDetail.objects.filter(name="org_name").first()
    org_description = OrgDetail.objects.filter(name="org_description").first()
    admin.site.site_title = org_name.value if org_name else "Organisation site admin"
    admin.site.site_header = (
        org_name.value if org_name else "Organisation Administration"
    )
    admin.site.index_title = (
        org_description.value if org_description else "Site administration"
    )


@receiver(post_save, sender=OrgDetail)
@receiver(post_delete, sender=OrgDetail)
def update_admin_site_titles(sender, **kwargs):
    set_admin_site_titles()

