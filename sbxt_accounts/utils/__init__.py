# accounts/utils/__init__.py

from model_utils import (
    get_bool,
    normalize_username,
    user_profile_media,
    format_name,
)

modules: list[str] = [
    get_bool.__doc__,
    normalize_username.__doc__,
    user_profile_media.__doc__,
    format_name.__doc__,
]  #: a list of docstrings for each imported model

__doc__: str = str("\n".join(modules))
