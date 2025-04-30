from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView, UpdateView

from .forms import (
    LoginForm,
    ProfileUpdateForm,
    SignUpForm,
)


class SignupPage(CreateView):
    form_class = SignUpForm
    template_name = "_auth/page.html"
    extra_context = {
        "signupinterface": True,
        "has_header": True,
        "has_footer": True,
        "page_title": [{"label": "Sign up", "url": None}],
    }

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("homepage")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.extra_context)
        context["next_redirect"] = self.request.GET.get("next", "")
        context["back_url"] = self.request.GET.get("back", "")
        return context

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error with your submission. Please check the form.",
        )
        return super().form_invalid(form)

    def form_valid(self, form):
        user = form.save()
        user.backend = settings.AUTHENTICATION_BACKENDS[0]  # Use the first backend
        login(self.request, user)
        messages.success(self.request, f"Welcome, {user.username}!")
        next_redirect = self.request.POST.get("next", "")
        if next_redirect:
            return redirect(next_redirect)
        return redirect("homepage")


class ProfileUpdatePage(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUpdateForm
    template_name = "_auth/page.html"  # Create this template
    success_url = reverse_lazy("profile_update")  # Redirect back to the same page

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["accounts_active"] = "active"
        context["profileupdate_active"] = "active"
        context["profileupdateinterface"] = "Update your credentials here"
        return context

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error with your submission. Please check the form.",
        )
        return super().form_invalid(form)

    def form_valid(self, form):
        user = form.save(commit=False)
        new_password = form.cleaned_data.get("new_password1")
        if new_password:
            user.set_password(new_password)
        user.save()  # Save the form with the uploaded image
        messages.success(
            self.request, "Profile updated successfully! Kindly log in again."
        )
        return redirect(self.success_url)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


def LoginPage(request):
    if request.user.is_authenticated:
        return redirect("homepage")

    extra_context = {
        "has_header": True,
        "has_footer": True,
        "logininterface": True,
        "page_title": [
            {"label": "Login", "url": None},  # current page
        ],
    }

    next_redirect = request.GET.get("next", "")
    back_url = request.GET.get("back", "")
    extra_context["next_redirect"] = next_redirect
    extra_context["back_url"] = back_url

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")

                next_redirect = request.POST.get("next", "")
                if next_redirect:
                    return redirect(next_redirect)
                return redirect("homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    extra_context["loginform"] = form
    return render(request, "_auth/page.html", extra_context)


@require_POST
def LogoutView(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect(settings.LOGOUT_REDIRECT_URL)
