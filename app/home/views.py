from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.db import connection
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import ContactForm
from .models import ListItem, Organization


def robots_txt(request):
    extra_context = {}
    return render(request, "home/robots.txt", extra_context, content_type="text/plain")


def HomePage(request):
    extra_context = {
        "has_header": True,
        "is_header_fixed": True,
        "has_contact": True,
        "has_footer": True,
        "list_items": ListItem.objects.filter(category__name="Offers"),
    }

    if request.method == "POST":
        filled_form = ContactForm(request.POST)
        if filled_form.is_valid():
            sender_name = filled_form.cleaned_data["name"]
            sender_email = filled_form.cleaned_data["email"]
            sender_subject = filled_form.cleaned_data["subject"]
            sender_message = filled_form.cleaned_data["message"]
            recipient_email = (
                Organization.objects.first().primary_email
                if Organization._meta.db_table in connection.introspection.table_names()
                else None,
            )

            email_context = {
                "name": sender_name,
                "email": sender_email,
                "subject": sender_subject,
                "message": sender_message,
                "url": request.build_absolute_uri(reverse("homepage")),
            }

            text_content = render_to_string("home/mail/mail_us.txt", email_context)
            html_content = render_to_string("home/mail/mail_us.html", email_context)

            msg = EmailMultiAlternatives(
                sender_subject,
                text_content,
                sender_email,
                [recipient_email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, "Your message has been sent. Thank you!")
            extra_context["contactform"] = ContactForm()
        else:
            messages.error(request, "There was an error sending the message")
            extra_context["contactform"] = ContactForm(request.POST)
    else:
        extra_context["contactform"] = ContactForm()

    return render(request, "home/page.html", extra_context)
