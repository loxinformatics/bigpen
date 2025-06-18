from django.urls import path

from .admin_site import portal_site
from .views import (
    ManifestView,
    SignUpView,
    mail_contact_us,
    signin,
    signout,
)

urlpatterns = [
    path("manifest.json", ManifestView.as_view(), name="webmanifest"),
    path("portal/", portal_site.urls, name="portal"),
    path("mail/contact-us/", mail_contact_us, name="mail_contact_us"),
    path("auth/signup/", SignUpView.as_view(), name="signup"),
    path("auth/signin/", signin, name="signin"),
    path("auth/signout/", signout, name="signout"),
]
