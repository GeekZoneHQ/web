"""
Django settings for web project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import environ

env = environ.Env(
    DEBUG=(bool, True),
)
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ")i@@^(m2b0jalyaa)r$2wg6o&mjb*rm_+cm9g03hyt=j61i2u("

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = [env("ALLOWED_HOSTS", default="localhost"), "127.0.0.1"]


# Application definition

# QUEUE
# DEADLETTER QUEUE

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "djangocookiebanner.cookiebanner",
    "livereload",
    "django.contrib.staticfiles",
    "tailwind",
    "theme",
    "widget_tweaks",
    # Included at the end so that we can configure
    # built-in django admin features
    "memberships",
    "django_extensions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "livereload.middleware.LiveReloadScript",
]

ROOT_URLCONF = "web.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "memberships.context_processors.recaptcha_enabled",
            ],
        },
    },
]

WSGI_APPLICATION = "web.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {"default": env.db(default="sqlite:/db.sqlite3")}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
        "OPTIONS": {
            "user_attributes": ("username", "email", "first_name", "last_name"),
            "max_similarity": 0.5,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 10,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = "static/"

STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY", default=None)
STRIPE_PUBLIC_KEY = env("STRIPE_PUBLIC_KEY", default=None)
SAND_PRICE_ID = env("SAND_PRICE_ID", default=None)
DONATION_PRODUCT_ID = env("DONATION_PRODUCT_ID", default=None)
RECAPTCHA_SITE_KEY = env("RECAPTCHA_SITE_KEY", default=None)
RECAPTCHA_SECRET_KEY = env("RECAPTCHA_SECRET_KEY", default=None)

LOGIN_URL = "memberships_login"
LOGIN_REDIRECT_URL = "memberships_details"
LOGOUT_REDIRECT_URL = "memberships_login"

TAILWIND_APP_NAME = "theme"

# Cookiebanner
# To specify the different Cookie Groups

from django.utils.translation import ugettext_lazy as _

COOKIEBANNER = {
    "title": _("Cookie preferences"),
    "header_text": _('We are using cookies on this website. To find out more, please read our <a href="https://geek.zone/tiki-index.php?page=Privacy%20Notice">privacy and cookie policy</a>.'),
    "groups": [
        {
            "id": "essential",
            "name": _("Essential"),
            "description": _("Essential cookies are necessary to provide our site and services and cannot be deactivated."),
            "cookies": [
                {
                    "pattern": "cookiebanner",
                    "description": _("Meta cookie for the cookies that are set."),
                },
                { 
                    "pattern": "csrftoken",
                    "description": _("- This cookie prevents Cross-Site-Request-Forgery attacks."),
                },
                {
                    "pattern": "sessionid",
                    "description": _("- This cookie is necessary to allow logging in, for example."),
                },          
           ],
        },
        {
            "id": "analytics",
            "name": _("Analytics"),
            "description": _("Analytical cookies provide anonymous statistics about how visitors navigate our site so we can improve site experience and performance."),
            "optional": True,
            "cookies": [
                {
                    "pattern": "_pk_.*",
                    "description": _("Matomo cookie for website analysis."),
                },
            ],
        },
    ],
}

# Celery Configuration Options
CELERY_TIMEZONE = "UTC"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
BROKER_URL = "django://"

# Email config
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "support@geek.zone"
EMAIL_HOST_PASSWORD = env("GMAIL_APP_PASSWORD", default=None)
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "Geek.Zone <support@geek.zone>"
