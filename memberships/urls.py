from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # path("/", views.home, name="memberships_home"),
    path("register/", views.register, name="register"),
    path("confirm/", views.confirm, name="confirm"),
    path("thanks/", views.thanks, name="thanks"),
    path("stripe-webhook/", views.stripe_webhook, name="stripe_webhook"),
    path("login/", views.login_view, name="memberships_login"),
    path("logout/", views.logout_view, name="memerships_logout"),
    # path("settings/", views.settings_view, name="memerships_settings")
]
