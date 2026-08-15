from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Prediction, UserProfile
from .forms import (RegisterForm,PredictionForm,ProfileForm,UserUpdateForm,)
from django.core.paginator import Paginator
from django.http import HttpResponse

from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.platypus import Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from ml_engine.predict import predict_loan

def home(request):

    return render(request, "index.html")
def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(

                username=form.cleaned_data["username"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"]

            )

            UserProfile.objects.create(
                user=user
            )

            messages.success(
                request,
                "Registration Successful."
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

            print("FORM IS VALID")

            prediction = form.save(commit=False)

            prediction.user = request.user

            # --------------------------------------------------
            # Feature Engineering
            # --------------------------------------------------

            if prediction.income_annum != 0:

                prediction.loan_income_ratio = (
                    prediction.loan_amount /
                    prediction.income_annum
                )

            else:

                prediction.loan_income_ratio = 0


            total_assets = (
                prediction.residential_assets_value +
                prediction.commercial_assets_value +
                prediction.luxury_assets_value +
                prediction.bank_asset_value
            )


            prediction.asset_loan_ratio = (
                total_assets /
                prediction.loan_amount
                if prediction.loan_amount != 0
                else 0
            )


            # --------------------------------------------------
            # Prepare Data for ML Model
            # --------------------------------------------------

            ml_data = {

                "no_of_dependents":
                    prediction.no_of_dependents,

                "education":
                    prediction.education,

                "self_employed":
                    prediction.self_employed,

                "income_annum":
                    prediction.income_annum,

                "loan_amount":
                    prediction.loan_amount,

                "loan_term":
                    prediction.loan_term,

                "cibil_score":
                    prediction.cibil_score,

                "residential_assets_value":
                    prediction.residential_assets_value,

                "commercial_assets_value":
                    prediction.commercial_assets_value,

                "luxury_assets_value":
                    prediction.luxury_assets_value,

                "bank_asset_value":
                    prediction.bank_asset_value,
            }


            # --------------------------------------------------
            # REAL ML PREDICTION
            # --------------------------------------------------

            try:

                ml_result = predict_loan(ml_data)

                print("ML RESULT:", ml_result)


                # --------------------------------------------------
                # Save ML Result
                # --------------------------------------------------

                prediction.prediction_result = (
                    ml_result["prediction"]
                )

                prediction.prediction_probability = (
                    ml_result["confidence"]
                )


                # --------------------------------------------------
                # Risk Level
                # --------------------------------------------------

                confidence = ml_result["confidence"]

# --------------------------------------------------
# Risk Level based on CIBIL Score
# --------------------------------------------------

                if prediction.cibil_score >= 700:

                    prediction.risk_level = "Low"

                elif prediction.cibil_score >= 600:

                    prediction.risk_level = "Medium"

                else:

                    prediction.risk_level = "High"
                prediction.status = "Completed"

                prediction.save()

                print(
                    "Prediction Saved:",
                    prediction.id
                )


                # --------------------------------------------------
                # Redirect to Result
                # --------------------------------------------------

                return redirect(
                    "result",
                    prediction.id
                )


            except Exception as e:

                print(
                    "ML PREDICTION ERROR:",
                    str(e)
                )

                form.add_error(
                    None,
                    "Unable to process the prediction. "
                    "Please try again."
                )


        else:

            print("FORM ERRORS:")
            print(form.errors)

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

    query = request.GET.get("search", "")

    filter_by = request.GET.get("filter", "all")

    predictions = Prediction.objects.filter(
        user=request.user
    )

    # Search
    if query:

        predictions = predictions.filter(

            Q(id__icontains=query) |
            Q(cibil_score__icontains=query) |
            Q(prediction_result__icontains=query) |
            Q(risk_level__icontains=query) |
            Q(status__icontains=query) |
            Q(loan_amount__icontains=query) |
            Q(income_annum__icontains=query)

        )

    # Filters
    if filter_by == "approved":

        predictions = predictions.filter(
            prediction_result="Approved"
        )

    elif filter_by == "rejected":

        predictions = predictions.filter(
            prediction_result="Rejected"
        )

    elif filter_by == "low":

        predictions = predictions.filter(
            risk_level="Low"
        )

    elif filter_by == "medium":

        predictions = predictions.filter(
            risk_level="Medium"
        )

    elif filter_by == "high":

        predictions = predictions.filter(
            risk_level="High"
        )

    predictions = predictions.order_by("-created_at")

    # Pagination
    paginator = Paginator(predictions, 10)

    page_number = request.GET.get("page")

    predictions = paginator.get_page(page_number)

    return render(
    request,
    "history.html",
    {
        "predictions": predictions,
        "query": query,
        "filter": filter_by,

        "total_predictions": Prediction.objects.filter(
            user=request.user
        ).count(),

        "approved_count": Prediction.objects.filter(
            user=request.user,
            prediction_result="Approved"
        ).count(),

        "rejected_count": Prediction.objects.filter(
            user=request.user,
            prediction_result="Rejected"
        ).count(),

        "low_count": Prediction.objects.filter(
            user=request.user,
            risk_level="Low"
        ).count(),

        "medium_count": Prediction.objects.filter(
            user=request.user,
            risk_level="Medium"
        ).count(),

        "high_count": Prediction.objects.filter(
            user=request.user,
            risk_level="High"
        ).count(),
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
@login_required
def download_report(request, prediction_id):

    prediction = get_object_or_404(
        Prediction,
        id=prediction_id,
        user=request.user
    )

    response = HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = (
        f'attachment; filename="NaNeVora_Report_{prediction.id}.pdf"'
    )

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    elements = []

    # ==========================
    # Heading
    # ==========================

    title = Paragraph(
        "<b><font size=18 color='blue'>NaNeVora</font></b>",
        styles["Title"]
    )

    subtitle = Paragraph(
        "<b>AI Loan Prediction Report</b>",
        styles["Heading2"]
    )

    elements.append(title)
    elements.append(subtitle)
    elements.append(Paragraph("<br/>", styles["Normal"]))

    # ==========================
    # Table Data
    # ==========================

    data = [

        ["Field", "Value"],

        ["Username", request.user.username],

        ["Dependents", prediction.no_of_dependents],

        ["Education", prediction.education],

        ["Self Employed", prediction.self_employed],

        ["Annual Income", f"₹ {prediction.income_annum:,}"],

        ["Loan Amount", f"₹ {prediction.loan_amount:,}"],

        ["Loan Term", prediction.loan_term],

        ["CIBIL Score", prediction.cibil_score],

        ["Residential Assets",
         f"₹ {prediction.residential_assets_value:,}"],

        ["Commercial Assets",
         f"₹ {prediction.commercial_assets_value:,}"],

        ["Luxury Assets",
         f"₹ {prediction.luxury_assets_value:,}"],

        ["Bank Assets",
         f"₹ {prediction.bank_asset_value:,}"],

        ["Loan Income Ratio",
         f"{prediction.loan_income_ratio:.2f}"],

        ["Asset Loan Ratio",
         f"{prediction.asset_loan_ratio:.2f}"],

        ["Prediction",
         prediction.prediction_result],

        ["Risk Level",
         prediction.risk_level],

        ["Confidence",
         f"{prediction.prediction_probability}%"],

        ["Status",
         prediction.status],

        ["Generated On",
         prediction.created_at.strftime("%d-%m-%Y %I:%M %p")]

    ]

    # ==========================
    # Create Table
    # ==========================

    table = Table(data, colWidths=[180, 250])

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("FONTSIZE", (0, 0), (-1, 0), 12),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),

            ("FONTSIZE", (0, 1), (-1, -1), 10),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ("BOTTOMPADDING", (0, 1), (-1, -1), 8),

        ])

    )

    elements.append(table)

    elements.append(Paragraph("<br/><br/>", styles["Normal"]))

    footer = Paragraph(

        "<font size='10'>Generated by NaNeVora AI Loan Assessment Platform</font>",

        styles["Normal"]

    )

    elements.append(footer)

    doc.build(elements)

    return response

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
@login_required
def result(request, prediction_id):

    prediction = get_object_or_404(
        Prediction,
        id=prediction_id,
        user=request.user
    )

    return render(
        request,
        "result.html",
        {
            "prediction": prediction
        }
    )

@login_required
def delete_prediction(request, prediction_id):

    prediction = get_object_or_404(
        Prediction,
        id=prediction_id,
        user=request.user
    )

    prediction.delete()

    messages.success(
        request,
        "Prediction deleted successfully."
    )

    return redirect("history")


def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")

        messages.success(
            request,
            "If this email exists, a password reset link will be sent."
        )

    return render(
        request,
        "forgot_password.html"
    )