from django.db import models
from django.contrib.auth.models import User


# ==========================================================
# User Profile
# ==========================================================

class UserProfile(models.Model):

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('mr', 'Marathi'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        blank=True,
        null=True
    )

    language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='en'
    )

    dark_mode = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username


# ==========================================================
# Loan Prediction
# ==========================================================

class Prediction(models.Model):

    EDUCATION = [
        ('Graduate', 'Graduate'),
        ('Not Graduate', 'Not Graduate'),
    ]

    YES_NO = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    RESULT = [
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='predictions'
    )

    no_of_dependents = models.IntegerField()

    education = models.CharField(
        max_length=20,
        choices=EDUCATION
    )

    self_employed = models.CharField(
        max_length=10,
        choices=YES_NO
    )

    income_annum = models.FloatField()

    loan_amount = models.FloatField()

    loan_term = models.IntegerField()

    cibil_score = models.IntegerField()

    residential_assets_value = models.FloatField()

    commercial_assets_value = models.FloatField()

    luxury_assets_value = models.FloatField()

    bank_asset_value = models.FloatField()

    # Feature Engineering (calculated in views.py)
    loan_income_ratio = models.FloatField(
        default=0
    )

    asset_loan_ratio = models.FloatField(
        default=0
    )

    prediction_result = models.CharField(
        max_length=20,
        choices=RESULT,
        blank=True
    )

    prediction_probability = models.FloatField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.username} - {self.prediction_result}"


# ==========================================================
# Free Trial
# ==========================================================

class GuestPrediction(models.Model):

    session_id = models.CharField(
        max_length=100
    )

    no_of_dependents = models.IntegerField()

    education = models.CharField(
        max_length=20
    )

    self_employed = models.CharField(
        max_length=10
    )

    income_annum = models.FloatField()

    loan_amount = models.FloatField()

    loan_term = models.IntegerField()

    cibil_score = models.IntegerField()

    residential_assets_value = models.FloatField()

    commercial_assets_value = models.FloatField()

    luxury_assets_value = models.FloatField()

    bank_asset_value = models.FloatField()

    prediction_result = models.CharField(
        max_length=20,
        blank=True
    )

    prediction_probability = models.FloatField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"Guest - {self.session_id}"