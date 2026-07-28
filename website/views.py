from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

from .models import Prediction, GuestPrediction, UserProfile
from .forms import (
    RegisterForm,
    PredictionForm,
    ProfileForm,
    UserUpdateForm,
)
def home(request):

    return render(request, "index.html")

def register(request):

    if request.user.is_authenticated:

        return redirect("dashboard")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            UserProfile.objects.create(user=user)

            messages.success(
                request,
                "Your account has been created successfully.. Please login."
            )

            return redirect("login")

    else:

        form = RegisterForm()

    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )

def login_view(request):

    if request.user.is_authenticated:

        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        else:

            messages.error(
                request,
                "Invalid Username or Password"
            )

    return render(request, "login.html")

@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect("home")

@login_required
def dashboard(request):

    # All predictions for statistics
    all_predictions = Prediction.objects.filter(
        user=request.user
    )

    # Only latest 5 predictions for display
    predictions = all_predictions.order_by(
        "-created_at"
    )[:5]

    context = {

        "predictions": predictions,

        "total_predictions": all_predictions.count(),

        "approved_count": all_predictions.filter(
            prediction_result="Approved"
        ).count(),

        "rejected_count": all_predictions.filter(
            prediction_result="Rejected"
        ).count(),

    }

    return render(
        request,
        "dashboard.html",
        context
    )
# ==========================================================
# Prediction
# ==========================================================

@login_required
def prediction(request):

    if request.method == "POST":

        form = PredictionForm(request.POST)

        if form.is_valid():

            prediction = form.save(commit=False)

            prediction.user = request.user

            # -----------------------------
            # Feature Engineering
            # -----------------------------

            prediction.loan_income_ratio = (
                prediction.loan_amount /
                prediction.income_annum
            )

            total_assets = (

                prediction.residential_assets_value +

                prediction.commercial_assets_value +

                prediction.luxury_assets_value +

                prediction.bank_asset_value

            )

            prediction.asset_loan_ratio = (

                total_assets /

                prediction.loan_amount

            )

            # -----------------------------
            # Temporary Result
            # ML Integration Later
            # -----------------------------

            prediction.prediction_result = "Approved"

            prediction.prediction_probability = 0.95

            prediction.save()

            messages.success(

                request,

                "Prediction completed successfully."

            )

            return redirect("dashboard")

    else:

        form = PredictionForm()

    return render(

        request,

        "prediction.html",

        {

            "form": form

        }

    )


# ==========================================================
# Prediction History
# ==========================================================

@login_required
def history(request):

    predictions = Prediction.objects.filter(

        user=request.user

    ).order_by("-created_at")

    return render(

        request,

        "history.html",

        {

            "predictions": predictions

        }

    )


# ==========================================================
# Profile
# ==========================================================

@login_required
def profile(request):

    profile = request.user.userprofile

    if request.method == "POST":

        user_form = UserUpdateForm(

            request.POST,

            instance=request.user

        )

        profile_form = ProfileForm(

            request.POST,

            request.FILES,

            instance=profile

        )

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()

            profile_form.save()

            messages.success(

                request,

                "Profile updated successfully."

            )

            return redirect("profile")

    else:

        user_form = UserUpdateForm(instance=request.user)

        profile_form = ProfileForm(instance=profile)

    context = {

        "user_form": user_form,

        "profile_form": profile_form

    }

    return render(

        request,

        "profile.html",

        context

    )


# ==========================================================
# Change Password
# ==========================================================

@login_required
def change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(

            request.user,

            request.POST

        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(

                request,

                user

            )

            messages.success(

                request,

                "Password changed successfully."

            )

            return redirect("profile")

    else:

        form = PasswordChangeForm(request.user)

    return render(

        request,

        "change_password.html",

        {

            "form": form

        }

    )

def contact(request):
    return render(request, "contact.html")


def privacy(request):
    return render(request, "privacy.html")


def terms(request):
    return render(request, "terms.html")

@login_required
def edit_profile(request):

    if request.method=="POST":

        form=EditProfileForm(

            request.POST,

            instance=request.user

        )

        if form.is_valid():

            form.save()

            messages.success(

                request,

                "Profile updated successfully."

            )

            return redirect("dashboard")

    else:

        form=EditProfileForm(

            instance=request.user

        )

    return render(

        request,

        "edit_profile.html",

        {

            "form":form

        }

    )

def download_report(request):
    return render(request, "download_report.html")


@login_required
def update_profile(request):

    if request.method == "POST":

        user = request.user

        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")

        user.save()

        messages.success(request, "Profile updated successfully.")

    return redirect("dashboard")