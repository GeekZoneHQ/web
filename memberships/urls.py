from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("confirm/", views.confirm, name="confirm"),
    path("thanks/", views.thanks, name="thanks"),
]
