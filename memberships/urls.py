from django.urls import path
from . import views
from django.contrib.auth.views import *
from django.urls import path, include

urlpatterns = [
    path("register/", views.register, name="register"),
    path("confirm/", views.confirm, name="confirm"),
    path("thanks/", views.thanks, name="thanks"),
    path("stripe-webhook/", views.stripe_webhook, name="stripe_webhook"),
    path("settings/", views.settings_view, name="memberships_settings"),
    path("details/", views.details_view, name="memberships_details"),
    path("verify", views.sendVerification, name="send_verification"),
    path("verify/<uidb64>/<token>", views.verify, name="verify"),
    path("change-password/", PasswordChangeView.as_view()),
    path(
        "login/",
        LoginView.as_view(template_name="memberships/login.html"),
        name="memberships_login",
    ),
    path(
        "logout/",
        LogoutView.as_view(template_name="memberships/logout.html"),
        name="memberships_logout",
    ),
]
