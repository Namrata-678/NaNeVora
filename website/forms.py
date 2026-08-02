from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from .models import Prediction, UserProfile
from django.contrib.auth.forms import SetPasswordForm

# ==========================================================
# Register Form
# ==========================================================
class RegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        widget=forms.PasswordInput()
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
        ]

    def clean(self):

        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned_data
def clean_username(self):

    username = self.cleaned_data["username"]

    if User.objects.filter(username=username).exists():

        raise forms.ValidationError(
            "Username already exists."
        )

    return username


def clean_email(self):

    email = self.cleaned_data["email"]

    if User.objects.filter(email=email).exists():

        raise forms.ValidationError(
            "Email already registered."
        )

    return email
# ==========================================================
# Prediction Form
# ==========================================================

class PredictionForm(forms.ModelForm):

    class Meta:
        model = Prediction
        exclude = [
            "user",
            "prediction_result",
            "prediction_probability",
            "loan_income_ratio",
            "asset_loan_ratio",
            "risk_level",
            "status",
            "created_at",
        ]


# ==========================================================
# User Update Form
# ==========================================================

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
        ]


# ==========================================================
# Profile Form
# ==========================================================

class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = "__all__"
        exclude = ["user"]

class EditProfileForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [

            'first_name',

            'last_name',

            'email'

        ]

class CustomPasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({

            "class": "form-control",

            "placeholder": "Enter your registered email",

            "autocomplete": "email",

            "required": True,

        })


class CustomSetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["new_password1"].widget.attrs.update({

            "class": "form-control",

            "placeholder": "Enter new password",

        })

        self.fields["new_password2"].widget.attrs.update({

            "class": "form-control",

            "placeholder": "Confirm new password",

        })
