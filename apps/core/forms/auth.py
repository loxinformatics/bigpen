from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UsernameField,
)

from ..management.config.auth import auth_config

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
