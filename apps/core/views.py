import json
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import View
from django.views.generic.edit import CreateView

from .forms import (
    MailUsForm,
    SignInForm,
    SignUpForm,
)
from .management.config.urls import urls_config
from .management.decorators import (
    auth_page_required,
    auth_page_required_class,
    redirect_authenticated_users,
    redirect_authenticated_users_class,
)
from .models import BaseDetail, BaseImage, ContactEmail

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class MailUsAPIView(View):
    """Handle contact form submission"""

    def post(self, request):
        try:
            # Parse JSON data
            data = json.loads(request.body)

            # Use Django form for validation
            form = MailUsForm(data)
            if not form.is_valid():
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Please correct the errors below.",
                        "errors": form.errors,
                    },
                    status=400,
                )

            # Extract validated data
            sender_name = form.cleaned_data["name"]
            sender_email = form.cleaned_data["email"]
            sender_subject = form.cleaned_data["subject"]
            sender_message = form.cleaned_data["message"]

            # Get recipient email
            recipient_email = None
            try:
                if hasattr(settings, "CONTACT_EMAIL"):
                    recipient_email = settings.CONTACT_EMAIL
                elif (
                    "ContactEmail" in globals()
                    and ContactEmail._meta.db_table
                    in connection.introspection.table_names()
                ):
                    contact_email_obj = ContactEmail.objects.filter(
                        is_primary=True
                    ).first()
                    if contact_email_obj:
                        recipient_email = contact_email_obj.email

                if not recipient_email:
                    recipient_email = getattr(
                        settings, "DEFAULT_FROM_EMAIL", "admin@example.com"
                    )
            except Exception as e:
                logger.error(f"Error getting recipient email: {str(e)}")
                recipient_email = getattr(
                    settings, "DEFAULT_FROM_EMAIL", "admin@example.com"
                )

            # Prepare email context
            email_context = {
                "name": sender_name,
                "email": sender_email,
                "subject": sender_subject,
                "message": sender_message,
                "url": request.build_absolute_uri("/"),
            }

            # Render email templates
            text_content = render_to_string("core/mail/contact.txt", email_context)
            html_content = render_to_string("core/mail/contact.html", email_context)

            # Send email
            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com")

            msg = EmailMultiAlternatives(
                f"Contact Form: {sender_subject}",
                text_content,
                from_email,
                [recipient_email],
                reply_to=[sender_email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return JsonResponse(
                {
                    "success": True,
                    "message": "Thank you for your message! We will get back to you soon.",
                }
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "message": "Invalid JSON data."}, status=400
            )

        except Exception as e:
            logger.error(f"Error sending contact email: {str(e)}")
            return JsonResponse(
                {
                    "success": False,
                    "message": "There was an error sending your message. Please try again later.",
                },
                status=500,
            )

    def get(self, request):
        """Optional: Handle GET requests"""
        return JsonResponse(
            {"success": False, "message": "Only POST requests are allowed."}, status=405
        )


class ManifestFile(View):
    """
    Returns a dynamically generated web manifest file.
    Cached for performance but always up-to-date.
    """

    def get(self, request):
        # Check cache first in production
        manifest_data = None
        if not settings.DEBUG:
            manifest_data = cache.get("manifest_data")

        if manifest_data is None:
            manifest_data = self.generate_manifest_data()

            # Cache in production only
            if not settings.DEBUG:
                cache.set("manifest_data", manifest_data, 60 * 15)  # 15 minutes

        response = JsonResponse(
            manifest_data, json_dumps_params={"indent": 2, "ensure_ascii": False}
        )
        response["Content-Type"] = "application/manifest+json"
        return response

    def generate_manifest_data(self):
        """Generate manifest data from database"""
        # Get values first
        name_value = self._get_detail_value("base_name", "")
        short_name_value = self._get_detail_value("base_short_name", "")
        description = self._get_detail_value("base_description", "A Django application")

        # Get theme_color without a default. If not found or empty, it will be None.
        theme_color = self._get_detail_value("base_theme_color", None)

        # short_name falls back to name in both cases
        name = short_name_value or name_value or "My App"
        short_name = short_name_value or name_value or "My App"

        # Get icons
        icons = self._generate_icons()

        manifest_data = {
            "name": name,
            "short_name": short_name,
            "description": description,
            "start_url": "/",
            "display": "standalone",
            # "background_color" is completely removed from here
            "icons": icons,
            "categories": ["productivity", "utilities"],
            "orientation": "portrait-primary",
            "scope": "/",
            "lang": "en",
        }

        # ONLY add theme_color if a value was retrieved from the database
        if (
            theme_color
        ):  # This checks if theme_color is not None and not an empty string
            manifest_data["theme_color"] = theme_color

        # The conditional addition for background_color is also removed.

        return manifest_data

    def _get_detail_value(self, name, default=""):
        """Get value from BaseDetail or return default"""
        try:
            detail = BaseDetail.objects.get(name=name)
            # This logic means if detail.value is an empty string,
            # it will fall back to `default`. If `default` is `None`,
            # then it will return `None` for empty strings.
            return detail.value or default
        except BaseDetail.DoesNotExist:
            return default

    def _generate_icons(self):
        """Generate icons array for manifest"""
        icons = []

        # Icon mappings: (model_name, sizes, type, purpose)
        icon_mappings = [
            ("base_favicon", "32x32", "image/png", "any"),
            ("base_apple_touch_icon", "180x180", "image/png", "any"),
            ("base_logo", "512x512", "image/png", "any"),
        ]

        for model_name, sizes, icon_type, purpose in icon_mappings:
            try:
                image_obj = BaseImage.objects.get(name=model_name)
                if image_obj.image:
                    # Directly use the image's URL
                    image_url = image_obj.image.url
                    icons.append(
                        {
                            "src": image_url,
                            "sizes": sizes,
                            "type": icon_type,
                            "purpose": purpose,
                        }
                    )
            except BaseImage.DoesNotExist:
                continue

        return icons


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
