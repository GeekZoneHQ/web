from web import settings


def recaptcha_enabled(request):
    return {
        "recaptcha_enabled": settings.RECAPTCHA_SECRET_KEY
        and settings.RECAPTCHA_SITE_KEY,
    }
