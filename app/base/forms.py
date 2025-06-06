from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import (
    AuthenticationForm,
    # UserChangeForm,
    UserCreationForm,
    UsernameField,
)

from .models import OrgDetail, OrgGraphic, SocialMediaLink


class UniqueChoiceFormMixin:
    """
    Mixin that filters choices to show only unused options for new instances.

    Requires:
    - model to have a 'name' field
    - model to have a CHOICES constant (e.g., ORG_DETAIL_CHOICES)
    - choices_attr: string name of the choices constant
    """

    choices_attr = None  # Override in subclass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk or not self.choices_attr:
            # If editing existing instance or no choices attr, don't modify choices
            return

        # Get the choices constant from the model
        model_choices = getattr(self._meta.model, self.choices_attr, [])

        # Get all existing values for this field
        existing_values = self._meta.model.objects.values_list("name", flat=True)

        # Filter out existing values from choices
        available_choices = [
            choice for choice in model_choices if choice[0] not in existing_values
        ]

        # Update the field choices
        self.fields["name"].choices = [(None, "")] + available_choices


class BaseOrgDetailForm(UniqueChoiceFormMixin, forms.ModelForm):
    choices_attr = "ORG_DETAIL_CHOICES"

    class Meta:
        model = OrgDetail
        fields = "__all__"


class BaseOrgGraphicForm(UniqueChoiceFormMixin, forms.ModelForm):
    choices_attr = "ORG_GRAPHIC_CHOICES"

    class Meta:
        model = OrgGraphic
        fields = "__all__"


class BaseSocialMediaLinkForm(UniqueChoiceFormMixin, forms.ModelForm):
    choices_attr = "SOCIAL_MEDIA_CHOICES"

    class Meta:
        model = SocialMediaLink
        fields = "__all__"
        exclude = ("icon",)


class AuthLoginForm(AuthenticationForm):
    # override the variables in BaseUserCreationform
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "form-control",
                "placeholder": "Your phone number",
            }
        )
    )
    password = forms.CharField(
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

    # remember_me = forms.BooleanField(
    #     required=False,
    #     initial=True,
    #     widget=forms.CheckboxInput(
    #         attrs={
    #             "class": "form-check-input",
    #         }
    #     ),
    #     label="Remember Me",
    # )


class AuthSignUpForm(UserCreationForm):
    # override the variables in BaseUserCreationform
    password1 = forms.CharField(
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
    password2 = forms.CharField(
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
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone number",
                }
            ),
        }


# class AuthProfileUpdateForm(UserChangeForm):
#     current_password = forms.CharField(
#         label="Current Password",
#         strip=False,
#         widget=forms.PasswordInput(
#             attrs={
#                 "class": "form-control",
#                 "placeholder": "Current Password",
#             },
#         ),
#     )
#     new_password1 = forms.CharField(
#         label="New Password",
#         strip=False,
#         widget=forms.PasswordInput(
#             attrs={
#                 "class": "form-control",
#                 "placeholder": "New Password",
#             },
#         ),
#     )
#     new_password2 = forms.CharField(
#         label="Confirm New Password",
#         strip=False,
#         widget=forms.PasswordInput(
#             attrs={
#                 "class": "form-control",
#                 "placeholder": "New Password Confirmation",
#             },
#         ),
#     )

#     class Meta:
#         model = get_user_model()
#         fields = ("username", "image", "first_name", "last_name")
#         widgets = {
#             "username": forms.TextInput(
#                 attrs={
#                     "class": "form-control",
#                     "placeholder": "Phone number",
#                 }
#             ),
#             "first_name": forms.TextInput(
#                 attrs={
#                     "class": "form-control",
#                     "placeholder": "First name",
#                 }
#             ),
#             "last_name": forms.TextInput(
#                 attrs={
#                     "class": "form-control",
#                     "placeholder": "Last name",
#                 }
#             ),
#             "image": forms.ClearableFileInput(
#                 attrs={
#                     "class": "form-control-file",  # Adjust class as needed
#                 }
#             ),
#         }

#     def clean_current_password(self):
#         current_password = self.cleaned_data.get("current_password")
#         if not self.instance.check_password(current_password):
#             raise forms.ValidationError("Incorrect current password.")
#         return current_password

#     def clean_new_password2(self):
#         new_password1 = self.cleaned_data.get("new_password1")
#         new_password2 = self.cleaned_data.get("new_password2")
#         if new_password1 and new_password2 and new_password1 != new_password2:
#             raise forms.ValidationError("New passwords do not match.")
#         return new_password2

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         new_password = self.cleaned_data.get("new_password1")
#         if new_password:
#             user.set_password(new_password)
#         if commit:
#             user.save()
#         return user
