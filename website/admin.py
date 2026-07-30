from django.contrib import admin
from .models import Prediction, UserProfile


# ==========================
# Prediction Admin
# ==========================

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "loan_amount",
        "cibil_score",
        "prediction_result",
        "risk_level",
        "prediction_probability",
        "created_at",
    )

    list_filter = (
        "prediction_result",
        "risk_level",
        "education",
        "self_employed",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "loan_income_ratio",
        "asset_loan_ratio",
        "prediction_probability",
        "created_at",
    )


# ==========================
# User Profile Admin
# ==========================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "dark_mode",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
    )

    ordering = (
        "-created_at",
    )