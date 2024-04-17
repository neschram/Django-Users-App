"""TestCases for :ref:`sbxt_accounts.models

Run these specific tests with ::

    python manage.py test sbxt_accounts.tests.test_accounts_models

"""

from django.test import TestCase
from sbxt_accounts.models import CustomAccount, AccountProfile
from .test_utils import TestUtils


class CustomAccountTestCase(TestCase):
    """CustomAccountTestCase

    TestCase suite for :class:`sbxt_accounts.models.CustomAccount`

    """

    def setUp(self):
        """setUp

        Set up the :class:`CustomAccountTestCase`

        creates users for testing:
            - superuser
            - staff user
            - normal user
        """

        self.superuser: CustomAccount.objects = TestUtils.get_superuser()
        self.staffuser: CustomAccount.objects = TestUtils.get_staff_user()
        self.normal_usr: CustomAccount.objects = TestUtils.get_normal_user()

    def test_no_username_raises_ValueError(self) -> None:
        """test_no_username_raises_ValueError(self)

        Verify that a ValueError is raised without `username`

        Checks that ``ValueError`` is raised when calling
        :func:`CustomAccount.objects.create_user()` without ``username``

        """
        username: str | None = None  #: username
        password: str = "P@55w0rd"  #: password

        with self.assertRaises(ValueError):
            """self.assertRaises(ValueError)"""
            CustomAccount.objects.create_user(
                username=username,
                password=password,
            )

    def test_no_password_raises_ValueError(self):
        """test_no_password_raises_ValueError(self)

        Verify that a ValueError is raised without `password`

        Checks that ``ValueError`` is raised when calling
        :func:`CustomAccount.objects.create_user()` without ``password``

        """
        username: str = "username"  #: username
        password: str = None  #: password

        with self.assertRaises(ValueError):
            CustomAccount.objects.create_user(
                username=username,
                password=password,
            )

    def test_superuser_must_be_staff(self):
        """test_superuser_must_be_staff(self)

        Verify that a superuser must also be staff

        Checks that ``ValueError`` is raised if ``is_staff``
        is ``False`` when calling :class:`CustomAccount.objects.create_superuser()`
        """
        username: str = "username"  #: username
        password: str = "P@55w0rd"  #: password
        is_staff: bool = False  #: is staff

        with self.assertRaises(ValueError):
            CustomAccount.objects.create_superuser(
                username=username,
                password=password,
                is_staff=is_staff,
            )

    def test_superuser_must_be_superuser(self):
        """test_superuser_must_be_superuser(self)

        Verify that a superuser must be a superuser

        Checks that `ValueError` is raised if ``is_superuser``
        is ``False`` when calling :func:`CustomAccount.objects.create_user()`
        """
        username: str = "username"  #: username
        password: str = "P@55w0rd"  #: password
        is_superuser: bool = False  #: is superuser

        with self.assertRaises(ValueError):
            CustomAccount.objects.create_superuser(
                username=username,
                password=password,
                is_superuser=is_superuser,
            )

    def test_create_superuser(self):
        """test_create_superuser(self)

        Verify the creation of a superuser

        Checks the following conditions for self.superuser:

        * is an instance of CustomAccount
        * is a superuser
        * is staff
        * is active
        * has a usable password

        """
        su: CustomAccount.objects = self.superuser  #: superuser
        self.assertIsInstance(su, CustomAccount)
        self.assertTrue(su.is_superuser)
        self.assertTrue(su.is_staff)
        self.assertTrue(su.is_active)
        self.assertTrue(su.has_usable_password())

    def test_create_staff_user(self):
        """test_create_staff_user(self)

        Verify the creation of a staff user

        Checks the following conditions for ``self.staffuser``:

        * is an instance of CustomAccount
        * is not a superuser
        * is staff
        * is active
        * has a usable password

        """
        stu: CustomAccount.objects = self.staffuser  #: staff user
        self.assertIsInstance(stu, CustomAccount)
        self.assertFalse(stu.is_superuser)
        self.assertTrue(stu.is_staff)
        self.assertTrue(stu.is_active)
        self.assertTrue(stu.has_usable_password())

    def test_create_normal_user(self):
        """test_create_normal_user(self)

        Verify the creation of a normal user

        Checks the following conditions for self.normie:

        * is an instance of CustomAccount
        * is not a superuser
        * is  not staff
        * is active
        * has a usable password

        Also verifies the following information:

        * ``__str__``
        * ``date_joined`` is not ``None``

        """
        nu: CustomAccount.objects = self.normie  #: normal user
        self.assertIsInstance(nu, CustomAccount)
        self.assertFalse(nu.is_superuser)
        self.assertFalse(nu.is_staff)
        self.assertTrue(nu.is_active)
        self.assertTrue(nu.has_usable_password())
        self.assertEqual(nu.__str__(), "normie")
        self.assertIsNotNone(nu.date_joined)


class AccountProfileTestCase(TestCase):
    """AccountProfileTestCase(TestCase)

    TestCase for :class:`sbxt_accounts.models.CustomAccount`

    """

    def setUp(self):
        # normal user information
        self.user: CustomAccount.objects = TestUtils.get_normal_user()
        self.fn: str = "Normal"
        self.ln: str = "User"
        self.e: str = "normaluser@test.dev"
        self.pn: str = "+18044448888"
        self.desc: str = "I am a pot grower!"

        # profile
        self.profile = AccountProfile.objects.create(
            user=self.user,
            first_name=self.fn,
            last_name=self.ln,
            email=self.e,
            phone=self.pn,
            description=self.desc,
        )

    def test_profile_requires_user(self):
        with self.assertRaises(AccountProfile.user.RelatedObjectDoesNotExist):
            AccountProfile.objects.create(
                user=None,
                first_name="Normalish",
                last_name="Users",
                email="normie2@test.dev",
                phone=self.pn,
                description=self.desc,
            )

    def test_profile_user_profile(self):
        self.assertEqual(self.user, self.profile.user)

    def test_profile_has_name(self):
        self.assertEqual(
            self.profile.first_name,
            self.fn,
        )
        self.assertEqual(
            self.profile.last_name,
            self.ln,
        )

    def test_profile_is_not_public(self):
        self.assertFalse(self.profile.is_public)
