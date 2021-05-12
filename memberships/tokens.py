import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    def _create_hash_value(self, user, timeStamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timeStamp)
            + six.text_type(user.username)
        )


email_verification_token = TokenGenerator()
