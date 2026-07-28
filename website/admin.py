from django.contrib import admin
from .models import Prediction, UserProfile, GuestPrediction


# ==========================================================
# Prediction Admin
# ==========================================================

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "loan_amount",
        "income_annum",
        "cibil_score",
        "prediction_result",
        "prediction_probability",
        "created_at",
    )

    list_filter = (
        "prediction_result",
        "education",
        "self_employed",
        "created_at",
    )

    search_fields = (
        "user__username",
        "prediction_result",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 20


# ==========================================================
# Guest Prediction Admin
# ==========================================================

@admin.register(GuestPrediction)
class GuestPredictionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "session_id",
        "loan_amount",
        "income_annum",
        "prediction_result",
        "prediction_probability",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 20


# ==========================================================
# User Profile Admin
# ==========================================================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "language",
        "dark_mode",
        "created_at",
    )

    search_fields = (
        "user__username",
    )

    ordering = (
        "-created_at",
    )