from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UsernameField,
)

from .management.config.auth import auth_config
from .models import ContactSocialLink


class MailUsForm(forms.Form):
    name = forms.CharField(
        label="Your Name",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Your Name"}
        ),
    )
    email = forms.EmailField(
        label="Your Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Your Email"}
        ),
    )
    subject = forms.CharField(
        label="Subject",
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Subject"}
        ),
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": "5", "placeholder": "Message"}
        ),
    )

    def clean_message(self):
        message = self.cleaned_data.get("message", "")
        if len(message.strip()) < 10:
            raise forms.ValidationError("Message must be at least 10 characters long.")
        return message


class UniqueChoiceFormMixin:
    """
    Mixin for forms that restricts the 'name' field choices to those not
    already used in the database, ensuring uniqueness.

    Expects `choices_attr` to be defined in subclasses, pointing to a list of allowed choices.
    """

    choices_attr = None  # Will be set dynamically in subclass

    def __init__(self, *args, **kwargs):
        """
        Initializes the form and dynamically filters available 'name' choices
        based on which ones are not already used in the database.
        """
        super().__init__(*args, **kwargs)

        if self.instance.pk or not self.choices_attr:
            return

        model_choices = getattr(self._meta.model, self.choices_attr, [])
        existing_values = self._meta.model.objects.values_list("name", flat=True)

        available_choices = [
            choice for choice in model_choices if choice[0] not in existing_values
        ]

        self.fields["name"].choices = [(None, "")] + available_choices


class ContactSocialLinkForm(UniqueChoiceFormMixin, forms.ModelForm):
    """
    Form for SocialMediaLink model, filtering out existing choices for 'name'.
    Excludes the 'icon' field from the form.
    """

    choices_attr = "SOCIAL_MEDIA_CHOICES"

    class Meta:
        model = ContactSocialLink
        fields = "__all__"
        exclude = ("icon",)


class SignInForm(AuthenticationForm):
    """
    Custom authentication form that applies dynamic labels and placeholders
    for the username field based on `auth_config`.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get username configuration from registry
        username_label = auth_config.get_username_label()
        username_placeholder = auth_config.get_username_placeholder()

        # Update the username field
        self.fields["username"] = UsernameField(
            label=username_label,
            widget=forms.TextInput(
                attrs={
                    "autofocus": True,
                    "class": "form-control",
                    "placeholder": username_placeholder,
                }
            ),
        )

        # Update password field
        self.fields["password"] = forms.CharField(
            label="Password",
            strip=False,
            widget=forms.PasswordInput(
                attrs={
                    "autocomplete": "current-password",
                    "class": "form-control",
                    "placeholder": "Your password",
                }
            ),
        )


class SignUpForm(UserCreationForm):
    """
    Custom user creation form that supports dynamic username labels/placeholders
    and styled input fields.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the registration form with dynamic username settings
        and customized password field widgets and help texts.
        """
        super().__init__(*args, **kwargs)

        # Get username configuration from registry
        username_label = auth_config.get_username_label()
        username_placeholder = auth_config.get_username_placeholder()

        # Update the username field
        self.fields["username"].label = username_label
        self.fields["username"].widget = forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": username_placeholder,
            }
        )

        # Update password fields
        self.fields["password1"] = forms.CharField(
            strip=False,
            widget=forms.PasswordInput(
                attrs={
                    "autocomplete": "new-password",
                    "class": "form-control",
                    "placeholder": "Password",
                }
            ),
            help_text=password_validation.password_validators_help_text_html(),
        )
        self.fields["password2"] = forms.CharField(
            widget=forms.PasswordInput(
                attrs={
                    "autocomplete": "new-password",
                    "class": "form-control",
                    "placeholder": "Password confirmation",
                }
            ),
            strip=False,
            help_text="Enter the same password as before, for verification.",
        )

    class Meta:
        model = get_user_model()
        fields = ("username",)
