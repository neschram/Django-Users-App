# accounts/validators.py

import re

from dateutil.relativedelta import relativedelta as rtimed
from datetime import datetime
from django.conf import settings
from django.contrib.auth.password_validation import CommonPasswordValidator
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


def validate_age(age: datetime.date) -> None:
    """validate_age

    Compares the provided `age` with the set `USER_AGE_LIMIT`.
    If age is the greater value, the date is newer than the
    required age and will raise a validation error.

    Args:
        age (datetime.date): age to validate

    Attributes:
        current_req (datetime.date): earliest date of birth
            to be of the required age

    Raises:
        ValidationError: age is greater than current_req
    """
    current_req: datetime = (datetime.now() - rtimed(settings.USER_AGE_LIMIT)).date()
    if age > current_req:
        raise ValidationError(
            _("%(value)s does not meet the current birth year: %(req)s"),
            params={"value": age, "req": current_req},
            code="age restriction",
        )


@deconstructible
class UsernameValidator(RegexValidator):
    """UsernameValidator

    Checks a desired username against a regular expression

    Username requirements:

        - Does not have an underscore (_) or period (.) at
        the beginning or end
        - Does not have simultaneous underscores or periods
        ex: "__" or ".."
        - Is between 8-20 characters
        - Only contains letters, numbers, underscores, or periods
    """

    regex: re.compile = r"^(?=[a-zA-Z0-9._]{8,20}$)(?!.*[_.]{2})[^_.].*[^_.]$"
    """regular expression"""

    message: str = _(
        "Enter a valid username. This value may contain only letters, "
        "numbers, and . or _ characters."
    )  #: message
    flags: int = 0  #: flags


class CustomCommonPasswordValidator(CommonPasswordValidator):
    """CustomCommonPasswordValidator

    Checks the users password against a list of commonly used passwords

    Raises:

        ValidationError: the password matched a common password

    Returns:

        None: the password was not found in common passwords

    """

    DEFAULT_PASSWORD_LIST_PATH: str = settings.COMMON_PASSWORDS_LIST
