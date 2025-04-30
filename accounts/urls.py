from django.urls import path

from .views import (
    LoginInterfaceView,
    LogoutInterfaceView,
    ProfileUpdateView,
    SignupView,
)

urlpatterns = [
    path("login/", LoginInterfaceView.as_view(), name="login"),
    path("logout/", LogoutInterfaceView.as_view(), name="logout"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("update/", ProfileUpdateView.as_view(), name="profile_update"),
]
