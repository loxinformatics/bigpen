from django import forms

from ..models.comments import Comment


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "email", "website", "content")
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Feature Coming Soon",
                    "disabled": "disabled",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Feature Coming Soon",
                    "disabled": "disabled",
                }
            ),
            "website": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Feature Coming Soon",
                    "disabled": "disabled",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "3",
                    "placeholder": "Feature Coming Soon",
                    "disabled": "disabled",
                }
            ),
        }
