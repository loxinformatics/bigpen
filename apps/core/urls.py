from django.urls import path

from . import views
from .admin import admin_site

urlpatterns = [
    path("portal/", admin_site.urls, name="portal"),
    path("mail/us/", views.MailUsAPIView.as_view(), name="mail_us"),
    path("auth/signup/", views.SignUpView.as_view(), name="signup"),
    path("auth/signin/", views.signin, name="signin"),
    path("auth/signout/", views.signout, name="signout"),
]
