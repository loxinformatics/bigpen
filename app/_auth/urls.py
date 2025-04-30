from django.urls import path

from .views import (
    LoginPage,
    LogoutView,
    ProfileUpdatePage,
    SignupPage,
)

urlpatterns = [
    path("login/", LoginPage, name="login"),
    path("logout/", LogoutView, name="logout"),
    path("signup/", SignupPage.as_view(), name="signup"),
    path("update/", ProfileUpdatePage.as_view(), name="profile_update"),
]
