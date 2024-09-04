from functools import (
    wraps,
)

from django.core.exceptions import (
    ValidationError,
)
from rest_framework.exceptions import (
    ValidationError as DRFValidationError,
)
from rest_framework.settings import (
    api_settings,
)


def handle_django_validation_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as exc:
            errors = None
            if hasattr(exc, 'error_dict'):
                errors = dict(exc)
            elif hasattr(exc, 'message'):
                errors = {api_settings.NON_FIELD_ERRORS_KEY: exc.message}

            if errors:
                raise DRFValidationError(errors) from exc

        return func

    return wrapper
