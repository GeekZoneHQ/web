from django.urls import path
from . import views
from django.contrib.auth.views import *

urlpatterns = [
    # path("/", views.home, name="memberships_home"),
    path("register/", views.register, name="register"),
    path("confirm/", views.confirm, name="confirm"),
    path("thanks/", views.thanks, name="thanks"),
    path("stripe-webhook/", views.stripe_webhook, name="stripe_webhook"),
    # path("login/", views.login_view, name="memberships_login"),
    # path("logout/", views.logout_view, name="memberships_logout"),
    path("settings/", views.settings_view, name="memberships_settings"),
    path('change-password/', PasswordChangeView.as_view()),
    path("login/", LoginView.as_view(template_name='memberships/login.html'), name="memberships_login"),
    path("logout/", LogoutView.as_view(template_name='memberships/logout.html'), name="memberships_logout"),

]
