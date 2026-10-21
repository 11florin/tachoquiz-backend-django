from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Category, RevisionNote

User = get_user_model()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        help_text = _(
            "Choose a username. Letters and numbers are recommended."
        )

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email address already exists."
            )

        return email


class RevisionNoteForm(forms.ModelForm):
    class Meta:
        model = RevisionNote
        fields = ["title", "category", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Enter a short title"}
            ),
            "content": forms.Textarea(
                attrs={"rows": 6, "placeholder": "Write your revision notes here..."}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.order_by("name_en")
        self.fields["category"].required = False
        self.fields["category"].empty_label = "General revision notes"
