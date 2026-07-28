from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Prediction, UserProfile


# ==========================================================
# Register Form
# ==========================================================

class RegisterForm(UserCreationForm):

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter First Name"
        })
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Last Name"
        })
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Email Address"
        })
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Choose Username"
        })

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Create Password"
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirm Password"
        })

    def clean_email(self):

        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email address is already registered."
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
