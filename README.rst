===============
Django User App
===============

A custom user app for a django application


Quick-Start
-----------

1. Import the app::

    python -m pip install ./sbxt_accounts

2. Add "accounts" to your INSTALLED_APPS settings::

    INSTALLED_APPS: list[str] = [
        ..., 
        "sbxt_accounts",
    ]

2. Set the user model in the settings file::

    AUTH_USER_MODEL: str = "sbxt_accounts.CustomAccount"

3. Set the user age limit in settings file::

    USER_AGE_LIMIT: int = 21

4. [Optional] Add the path to your common passwords and add the custom common password validator in settings::

    COMMON_PASSWORDS_LIST: str = "path/to/common_passwords_list.txt"

    AUTH_PASSWORD_VALIDATORS: list[dict[str,str]] = [
        ...,
        {
            "NAME": "accounts.validators.CustomCommonPasswordValidator",
        },
    ]

5. 
