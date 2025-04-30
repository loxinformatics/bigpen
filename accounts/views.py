from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from .forms import (
    CustomUserAuthenticationForm,
    CustomUserChangeForm,
    CustomUserCreationForm,
)
from .models import CustomUser


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/registration.html"
    success_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("home")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["accounts_active"] = "active"
        context["signup_active"] = "active"
        context["signupinterface"] = "Sign up here"
        return context

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error with your submission. Please check the form.",
        )
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Signup successful! You can now log in.")
        return response


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "accounts/registration.html"  # Create this template
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
        messages.success(self.request, "Profile updated successfully! Kindly log in again.")
        return redirect(self.success_url)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class LoginInterfaceView(LoginView):
    template_name = "accounts/registration.html"
    authentication_form = CustomUserAuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["accounts_active"] = "active"
        context["login_active"] = "active"
        context["logininterface"] = "Enter your credentials here"
        return context

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Incorrect username/email or password.",
        )
        return super().form_invalid(form)


class LogoutInterfaceView(LogoutView):
    template_name = "accounts/registration.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["accounts_active"] = "active"
        context["logout_active"] = "active"
        context["logoutinterface"] = "You've logged out :)"
        return context
