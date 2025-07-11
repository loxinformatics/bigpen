from django.urls import path

from .admin.site import admin_site
from .views.auth import SignUpView, signin, signout
from .views.mail import MailUsAPIView

urlpatterns = [
    path("portal/", admin_site.urls, name="portal"),
    path("mail/us/", MailUsAPIView.as_view(), name="mail_us"),
    path("auth/signup/", SignUpView.as_view(), name="signup"),
    path("auth/signin/", signin, name="signin"),
    path("auth/signout/", signout, name="signout"),
]
