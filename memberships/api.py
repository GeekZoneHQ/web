from jwt import encode, decode
from rest_framework.parsers import JSONParser
from datetime import datetime, timedelta
from django.conf import settings
from .responses import ERROR_CODE_ENUM
from django.contrib.auth.models import User


def verifyPostMethod(httpMethod):
    if httpMethod != "POST":
        raise ERROR_CODE_ENUM.METHOD_NOT_ALLOWED.throw()


def jsonFromRequest(request):
    try:
        return JSONParser().parse(request)
    except:
        raise ERROR_CODE_ENUM.MALFORMED_JSON.throw()


def verifyPasswordSignonRequestBody(body):
    if "email" not in body.keys() or "password" not in body.keys():
        raise ERROR_CODE_ENUM.MISSING_CREDENTIALS.throw()


def checkPasswordForUserWithEmail(email, password):
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            return True
        else:
            raise ERROR_CODE_ENUM.FORBIDDEN.throw()
    except:
        raise ERROR_CODE_ENUM.FORBIDDEN.throw()


def createAccessToken(email):
    tokenExpiry = str(
        (
            datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY)
        ).isoformat()
    )
    accessToken = encode(
        {
            "email": email,
            "expiry": tokenExpiry,
        },
        settings.JWT_SECRET,
        algorithm="HS256",
    )

    return accessToken, tokenExpiry


def createRefreshToken(email):
    return encode(
        {
            "email": email,
            "expiry": str(
                (
                    datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRY)
                ).isoformat()
            ),
        },
        settings.JWT_SECRET,
        algorithm="HS256",
    )
