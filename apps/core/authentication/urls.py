from django.urls import path

from .views import (
    SignUp,
    signin,
    signout,
)

app_name = "auth"

urlpatterns = [
    path("signup", SignUp.as_view(), name="signup"),
    path("signin", signin, name="signin"),
    path("signout", signout, name="signout"),
]
