import functools

from jwt import encode
from rest_framework.parsers import JSONParser, ParseError
from datetime import datetime, timedelta
from django.conf import settings
from .responses import ErrorCodeEnum, APIError
from django.contrib.auth.models import User
from django.http import JsonResponse


def api_response(func):
    """
    Decorator to allow API methods to have custom error responses while allowing web views to remain
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> JsonResponse:
        try:
            response = func(*args, **kwargs)
        except APIError as err:
            err.log()
            response = err.to_response()
        except Exception as e:
            print(e)
            response = ErrorCodeEnum.INTERNAL_SERVER_ERROR.value.to_response()
        return response

    return wrapper


def verify_post_method(http_method: str) -> None:
    """
    Verifies the HTTP method is 'POST'
    :raises APIError: if http_method is not equal to 'POST'
    """
    if http_method != "POST":
        raise APIError(ErrorCodeEnum.METHOD_NOT_ALLOWED)


def json_from_request(request):
    try:
        return JSONParser().parse(request)
    except ParseError:
        raise APIError(ErrorCodeEnum.MALFORMED_JSON)


def verify_property_is_str(body: dict, key: str) -> bool:
    if type(body.get(key)) != str:
        return False
    return True


def verify_password_signon_request_body(body):
    if "email" not in body.keys() or "password" not in body.keys():
        raise APIError(ErrorCodeEnum.MISSING_CREDENTIALS)

    if not verify_property_is_str(body, "email"):
        raise APIError(ErrorCodeEnum.INVALID_TYPE)

    if not verify_property_is_str(body, "password"):
        raise APIError(ErrorCodeEnum.INVALID_TYPE)


def check_password_for_user_with_email(email: str, password: str) -> bool:
    """
    Checks whether the password is correct for the given users email
    """
    user: User = User.objects.get(email=email)
    if user.check_password(password):
        return True
    return False


def create_access_token(email: str) -> tuple[dict, str]:
    """
    Creates an access token for the given email
    :return: the access token and it's expiry
    """
    token_expiry = str(
        (
                datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY)
        ).isoformat()
    )
    access_token = encode(
        {
            "email": email,
            "expiry": token_expiry,
        },
        settings.JWT_SECRET,
        algorithm="HS256",
    )

    return access_token, token_expiry


def create_refresh_token(email: str) -> str:
    """
    Creates a refresh token for a given email
    :return: the refresh token
    """
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
