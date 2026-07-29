from django.contrib import admin
from .models import UserProfile, Prediction


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "created_at",
        "dark_mode",
    )

    search_fields = (
        "user__username",
    )


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "prediction_result",
        "prediction_probability",
        "created_at",
    )

    list_filter = (
        "prediction_result",
        "education",
        "self_employed",
    )

    search_fields = (
        "user__username",
    )