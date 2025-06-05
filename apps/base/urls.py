from django.urls import path

from .views import SignUp, home, signin, signout

app_name = "base"

urlpatterns = [
    path("signup", SignUp.as_view(), name="signup"),
    path("signin", signin, name="signin"),
    path("signout", signout, name="signout"),
    path("", home, name="home"),
]
