from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        help_texts = {
            "username": (
                "Choose a username. Letters and numbers are recommended."
            ),
        }

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email address already exists."
            )

        return email