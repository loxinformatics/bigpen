from django import forms

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


class SiteDetailForm(UniqueChoiceFormMixin, forms.ModelForm):
    choices_attr = "ORG_DETAIL_CHOICES"

    class Meta:
        model = OrgDetail
        fields = "__all__"


class SiteGraphicForm(UniqueChoiceFormMixin, forms.ModelForm):
    choices_attr = "ORG_GRAPHIC_CHOICES"

    class Meta:
        model = OrgGraphic
        fields = "__all__"


class SocialMediaLinkForm(UniqueChoiceFormMixin, forms.ModelForm):
    choices_attr = "SOCIAL_MEDIA_CHOICES"

    class Meta:
        model = SocialMediaLink
        fields = "__all__"
        exclude = ("icon",)
