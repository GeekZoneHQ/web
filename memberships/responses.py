from django.template.response import SimpleTemplateResponse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from enum import Enum


class APIError(Exception):
    def __init__(
        self,
        status=500,
        errorCode=5999,
        errorMessage="Internal Server Error",
        cause=None,
    ):
        self.status = status
        self.errorCode = errorCode
        self.errorMessage = errorMessage
        self.cause = cause

    def toResponse(self, headers=None):
        return JsonResponse(
            status=self.status,
            headers=headers,
            data={
                "status": self.status,
                "errorCode": str(self.errorCode),
                "errorMessage": self.errorMessage,
            },
        )

    def log(self):
        print(
            f"Request failed with status: {self.status}, errorCode: {self.errorCode} and errorMessage: {self.errorMessage}. Cause: {self.cause}"
        )


class ERROR_CODE_ENUM(Enum):
    MISSING_CREDENTIALS = APIError(400, 4001, "Credentials missing from JSON body")
    MALFORMED_JSON = APIError(400, 4002, "Malformed JSON body")
    FORBIDDEN = APIError(403, 4031, "Forbidden")
    METHOD_NOT_ALLOWED = APIError(405, 4051, "Method not allowed")
    INTERNAL_SERVER_ERROR = APIError(500, 5999, "Internal Server Error")

    def throw(self):
        raise self.value
