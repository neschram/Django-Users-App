"""sbxt_accounts/utils/test_utils.py

    Utilities for "class"`django.test.TestCase` tests required to test
    :ref:`sbxt_accounts.models.CustomAccount`

"""

from typing import Optional
from sbxt_accounts.models import CustomAccount as User


class TestUtils:
    def get_superuser(u: Optional[str] = None, p: Optional[str] = None) -> User:
        if u is None:
            u: str = "superuser"  #: superuser username
        if p is None:
            p: str = "P@55w0rd"  #: superuser password
        s: User.objects = User.objects.create_superuser(
            username=u,
            password=p,
        )

        return s

    def get_staff_user(
        u: Optional[str] = "staffuser",
        p: Optional[str] = "P@55w0rd",
    ) -> User:
        su: User.objects = User.objects.create_user(
            username=u,
            password=p,
            is_staff=True,
        )

    def get_normal_user(
        u: Optional[str] = "normie",
        p: Optional[str] = "P@55w0rd",
    ) -> User:
        nu: User.objects = User.objects.create_user(
            username=u,
            password=p,
        )
