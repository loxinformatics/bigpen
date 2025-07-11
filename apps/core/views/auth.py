from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView

from ..decorators.auth import (
    auth_page_required,
    auth_page_required_class,
    redirect_authenticated_users,
    redirect_authenticated_users_class,
)
from ..forms.auth import SignInForm, SignUpForm
from ..management.config.urls import urls_config


@auth_page_required("signin")
@redirect_authenticated_users
def signin(request):
    """
    Handle user sign-in.

    - Redirects authenticated users via decorator.
    - On GET, render the sign-in form.
    - On POST, authenticate the user and log them in if credentials are valid.
    - If authentication fails, show an error message.
    """

    extra_context = {
        "page_title": "Login",
        "header_auth_btn": False,
        "show_auth": "signin",
        "overlay_whatsapp_call_us": False,
    }

    next = request.GET.get("next", "")
    back = request.GET.get("back", "")
    extra_context["next"] = next
    extra_context["back"] = back

    if request.method == "POST":
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next = request.POST.get("next", "")
                if next:
                    return redirect(next)
                return redirect(urls_config.get_login_redirect_url_safe())
            else:
                messages.error(
                    request, "Invalid username or password.", extra_tags="signin"
                )
        else:
            messages.error(
                request, "Invalid username or password.", extra_tags="signin"
            )
    else:
        form = SignInForm()

    extra_context["loginform"] = form
    return render(request, "core/index.html", extra_context)


@require_POST
def signout(request):
    """
    Log out the current user and redirect to the landing page
    with a success message.
    """
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect(urls_config.get_landing_url_name())


@auth_page_required_class("signup")
@redirect_authenticated_users_class
class SignUpView(CreateView):
    """
    Handle user registration.

    - Displays the signup form on GET.
    - Creates and logs in the user on valid POST.
    - Displays an error message on form error.
    - Redirects to the next page if specified or to the sign-in page otherwise.
    """

    form_class = SignUpForm
    template_name = "core/index.html"
    extra_context = {
        "page_title": "Sign up",
        "header_auth_btn": False,
        "show_auth": "signup",
        "overlay_whatsapp_call_us": False,
    }

    def get_context_data(self, **kwargs):
        """
        Add extra context including navigation flow (next/back).
        """
        context = super().get_context_data(**kwargs)
        context.update(self.extra_context)
        context["next"] = self.request.GET.get("next", "")
        context["back"] = self.request.GET.get("back", "")
        return context

    def form_invalid(self, form):
        """
        Display error message if form submission is invalid.
        """
        messages.error(
            self.request,
            "There was an error with your submission. Please check the form.",
            extra_tags="signup",
        )
        return super().form_invalid(form)

    def form_valid(self, form):
        """
        Create the user, log them in, and redirect based on flow.
        """
        user = form.save()
        user.backend = settings.AUTHENTICATION_BACKENDS[0]  # Optional but useful
        login(self.request, user)

        next = self.request.POST.get("next", "")
        if next:
            return redirect(next)

        return redirect("signin")
