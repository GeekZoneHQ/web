from django.http import JsonResponse
from enum import Enum
from typing import Dict


class ErrorCode:
    def __init__(self, status: int, code: int, message: str):
        self.status = status
        self.code = code
        self.message = message


class ErrorCodeEnum(Enum):
    MISSING_CREDENTIALS = ErrorCode(400, 4001, "Credential missing from JSON body")
    MALFORMED_JSON = ErrorCode(400, 4002, "Malformed JSON body")
    INVALID_TYPE = ErrorCode(400, 4003, "Property missing from JSON body")
    FORBIDDEN = ErrorCode(403, 4031, "Forbidden")
    METHOD_NOT_ALLOWED = ErrorCode(405, 4051, "Method not allowed")
    INTERNAL_SERVER_ERROR = ErrorCode(500, 5999, "Internal Server Error")


class APIError(Exception):
    """
    An error which can be thrown containing information about both the cause and the response to be returned.
    """

    def __init__(self, error_code: ErrorCodeEnum, override_message: str = None, cause: Exception = None):
        self.status = error_code.value.status
        self.code = error_code.value.code
        self.message = override_message if override_message else error_code.value.message
        self.cause = cause

    def to_response(self, headers: Dict = None) -> JsonResponse:
        """
        Helper method to create a JSON response based on the error thrown.
        """
        return JsonResponse(
            status=self.status,
            headers=headers,
            data={
                "status": self.status,
                "errorCode": str(self.code),
                "errorMessage": self.message,
            },
        )

    def log(self) -> None:
        """
        Helper method to log details about the error response and cause.
        """
        print(f"""Request failed with status: {self.status}, errorCode: {self.code} and errorMessage: {self.message}.
                {'Cause: ' + str(self.cause) if self.cause else ''}""")
