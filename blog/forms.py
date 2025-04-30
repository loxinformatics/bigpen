from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms

from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        widgets = {
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            )
        }


class SearchForm(forms.Form):
    text = forms.CharField(
        max_length=255,
        label="",
        widget=forms.TextInput(attrs={}),
    )


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "email", "website", "content")
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your Name*",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your Email*",
                }
            ),
            "website": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "Your Website"}
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "3",
                    "placeholder": "Your Comment*",
                }
            ),
        }
