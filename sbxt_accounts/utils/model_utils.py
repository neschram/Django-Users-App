"""accounts/utils/model_utils.py

Utilities designed to assist with sbxt_accounts models
"""

from typing import Optional


def get_bool(v: bool, alt: Optional[tuple[str, str]] = ("active", "inactive")) -> str:
    """human-readable format for any boolean values

    defaults to the status values ``"active"`` and ``"inactive"``

    :param v: `True`/`False` boolean value
    :type v: bool
    :param alt: optional (True, False) replacement of return values
    :type alt: str

    Examples::

        >>> from core.utils import print_bool
        >>> print_bool(True)
        "active"
        >>> print_bool(False, alt=("yes","no"))
        "no"

    """

    t, f = alt

    return t if v else f


def normalize_username(username: str) -> str:
    """normalize_username(self, username: str) -> str

    Strips a username string of whitespace and lowercases the characters

    :param username: username
    :type username: str
    :return: the lowercased value of username stripped of whitespace
    :rtype: str

    Example::

        >>> from accounts.managers.GrowOpUserManager import normalize_username
        >>> normalize_username(username="That awesome guy")
        "that_awesome_guy"

    """
    return "_".join([n.strip() for n in username.lower().strip().split()])


def user_profile_media(instance, filename):
    """user_profile_media

    Args:
        instance (UserProfile): the profile image's instance
        filename (str): the uploaded file's name

    Returns:
        str: a relative path to the media file
    """
    return "users/profile/{0}/{1}".format(instance.user, filename)


def format_name(n: str) -> str:
    """format_name(n: str) -> str

    Capitalizes only the first character and leaves all other
    characters as they were.

    Args:
        n (str): the text to format

    Returns:
        str: formatted `n`




    Example::

        >>> from core.utils import format_name
        >>> format_name("mcDaniel")
        "McDaniel"

    """

    formatted_n: str = "".join([n.upper()[0], n[1:]])

    return formatted_n
