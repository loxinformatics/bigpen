# from .models import Item
# from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserChangeForm as BaseUserChangeForm,
)
from django.contrib.auth.models import Group

from apps.core.management.config.auth import auth_config

# ============================================================================
# AUTH FORMS
# ============================================================================


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = get_user_model()
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Update username field (assuming auth_config is defined elsewhere)
        self.fields["username"].label = f"Username / {auth_config.get_username_label()}"
        self.fields["username"].widget.attrs["placeholder"] = (
            auth_config.get_username_placeholder()
        )

        # Filter groups field to hide "superuser" group for non-superusers
        if "groups" in self.fields:
            # Get the current user from the form's initial data or from the request
            # You'll need to pass the request user to the form (see admin class modification below)
            current_user = getattr(self, "_current_user", None)

            if current_user and not current_user.is_superuser:
                # Exclude the "superuser" group from the queryset
                self.fields["groups"].queryset = Group.objects.exclude(name="superuser")
        # Filter groups to only show UserRole instances in the admin
        # if "groups" in self.fields:
        #     self.fields["groups"].queryset = UserRole.objects.all()

    # def clean_groups(self):
    #     """Ensure user is assigned to exactly one role group."""
    #     groups = self.cleaned_data.get("groups")

    #     if not groups:
    #         raise forms.ValidationError(
    #             "This field is required. Please select at least one group."
    #         )

    #     # Check that only one role group is selected
    #     role_groups = list(groups)

    #     if len(role_groups) > 1:
    #         role_names = [g.name for g in role_groups]
    #         raise forms.ValidationError(
    #             f"User can only be assigned to one role group. "
    #             f"You selected: {', '.join(role_names)}. "
    #             f"Please select only one role group."
    #         )

    #     return groups


# class OrderForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.items = Item.objects.all()  # Store queryset for validation later
#         for item in self.items:
#             self.fields[f"item_{item.id}"] = forms.IntegerField(
#                 label=f"{item.name} (In Stock: {item.quantity})",
#                 min_value=0,
#                 initial=0,
#                 required=False,
#             )

#     def clean(self):
#         cleaned_data = super().clean()
#         for item in self.items:
#             field_name = f"item_{item.id}"
#             quantity = cleaned_data.get(field_name)
#             if quantity and quantity > item.quantity:
#                 self.add_error(
#                     field_name,
#                     f"Only {item.quantity} left in stock for '{item.name}'.",
#                 )
#         return cleaned_data
