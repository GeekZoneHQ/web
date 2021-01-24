# import django_email_verification
from django.urls import path
from . import views
from django.contrib.auth.views import *
from django.urls import path, include
from django_email_verification import urls as email_urls


urlpatterns = [
    path("register/", views.register, name="register"),
    path("confirm/", views.confirm, name="confirm"),
    path("thanks/", views.thanks, name="thanks"),
    path("stripe-webhook/", views.stripe_webhook, name="stripe_webhook"),
    path("settings/", views.settings_view, name="memberships_settings"),
    path("details/", views.details_view, name="memberships_details"),
    path("verify/", views.verify_email, name="verify_email"),
    # path("verify-token/", views.email_token_verification, name="verify_email_template"),
    # path("verify-token/", lambda request: render(request, 'verify_email_template.html')),
    # path('<str:email>/<str:email_token>', views.email_token_verification),
    path('email/', include(email_urls)),
    path('change-password/', PasswordChangeView.as_view()),
    path("login/", LoginView.as_view(template_name='memberships/login.html'), name="memberships_login"),
    path("logout/", LogoutView.as_view(template_name='memberships/logout.html'), name="memberships_logout"),


]
