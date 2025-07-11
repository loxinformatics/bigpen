import json
import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import connection
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from ..forms.mail import MailUsForm
from ..models.contact import ContactEmail

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
