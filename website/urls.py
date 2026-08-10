from django.urls import path
from django.contrib.auth import views as auth_views
from . import forms
from . import views

urlpatterns = [

    # ==========================
    # Home
    # ==========================
    path('', views.home, name='home'),

    # ==========================
    # Contact
    # ==========================
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),

    # ==========================
    # Authentication
    # ==========================
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ==========================
    # Dashboard
    # ==========================
    path('dashboard/', views.dashboard, name='dashboard'),

    # ==========================
    # Loan Prediction
    # ==========================
    path('prediction/', views.prediction, name='prediction'),

    # ==========================
    # Prediction History
    # ==========================
    path('history/', views.history, name='history'),
    # If your navbar uses 'prediction_history', add this alias too:
    path('prediction-history/', views.history, name='prediction_history'),

    # ==========================
    # User Profile
    # ==========================
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),

    path( "edit-profile/",views.edit_profile,name="edit_profile"),

    path("download-report/",views.download_report,name="download_report"),
   
    path(
    "update-profile/",
    views.update_profile,
    name="update_profile",
    ),
    path(
    "result/<int:prediction_id>/",
    views.result,
    name="result"
    ),

    path(
    "delete-prediction/<int:prediction_id>/",
    views.delete_prediction,
    name="delete_prediction",
    ),
    path(
    "download-report/<int:prediction_id>/",
    views.download_report,
    name="download_report"
    ),
# ==========================
# Forgot Password
# ==========================

path(
    "forgot-password/",
    auth_views.PasswordResetView.as_view(
        template_name="forgot_password.html",
        form_class=forms.CustomPasswordResetForm,
    ),
    name="forgot_password",
),

path(
    "forgot-password/done/",
    auth_views.PasswordResetDoneView.as_view(
        template_name="password_reset_done.html"
    ),
    name="password_reset_done",
),

path(
    "reset/<uidb64>/<token>/",
    auth_views.PasswordResetConfirmView.as_view(
        template_name="password_reset_confirm.html"
    ),
    name="password_reset_confirm",
),

path(
    "reset/done/",
    auth_views.PasswordResetCompleteView.as_view(
        template_name="password_reset_complete.html"
    ),
    name="password_reset_complete",
),
]