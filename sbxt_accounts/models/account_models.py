#  accounts/models/account_models.py

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db.models import (
    CharField,
    BooleanField,
    DateTimeField,
    SlugField,
)
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from sbxt_accounts.utils import get_bool, normalize_username
from sbxt_accounts.validators import UsernameValidator


class CustomAccountManager(BaseUserManager):
    """CustomUserManager

    Custom user model manager for authentication
    """

    def create_user(
        self,
        username: str,
        password: str,
        **extra_fields,
    ) -> BaseUserManager.create:
        """CustomUserManager.create_user

        Args:
            username (str): username
            password (str): password

        Raises:
            ValueError: missing username or password

        Returns:
            BaseUserManager.create: create a user instance
        """

        check_list: dict = {
            username: _("username must be set"),
            password: _("password must be set"),
        }

        for k, v in check_list.items():
            if not k:
                raise ValueError(v)

        username: str = username.lower()
        user: self.model = self.model(
            username=username, password=password, **extra_fields
        )  #: user
        user.set_password(password)
        user.save()

        return user

    def create_superuser(
        self,
        username: str,
        password: str,
        **extra_fields,
    ) -> BaseUserManager.create:
        """CustomUserManager.create_superuser

        Sets default fields to `True`:

            - is_active
            - is_staff
            - is_superuser

        Args:

            username (str): username
            password (str): password
            **extra_fields (dict): additional model fields with data

        Raises:

            ValueError: is_staff = False
            ValueError: is_superuser = False
            ValueError: is_active = False

        Returns:
            BaseUserManager.create: a new superuser user instance
        """

        # identify superuser fields
        su_extras: tuple[str, str] = [
            ("is_staff", _("Superuser must have is_staff=True")),
            ("is_superuser", "Superuser must have is_superuser=True"),
            ("is_active", "Superuser must have is_active=True"),
        ]  #: required extra fields for superuser

        # set and verify default superuser fields
        for f, e in su_extras:
            # set the field to `True`
            extra_fields.setdefault(f, True)
            if extra_fields.get(f) is not True:
                # raise ValueEror if field is not set
                raise ValueError(e)

        return self.create_user(
            username=username, password=password, extra_fields=extra_fields
        )


class CustomAccount(AbstractBaseUser, PermissionsMixin):
    """CustomAccount

    Custom user model:

    Extends from Django's abstract base user model with the following changes:

    Adds:
        date_joined (DateTimeField): datetime of account creation
        last_logout (DateTimeField): datetime of last account logout

    .. warning::
        Be cautious using `is_staff` and `is_superuser` as
        users with these values set to `True` will be able to make
        irrevocable changes.

    Returns:
        CustomAccount (object): A user account
    """

    class Meta:
        """Meta data for the CustomAccount model"""

        db_table: str = "accounts"
        db_table_comment: str = "user accounts"
        managed: bool = True
        verbose_name: str = _("accounts")
        # additional options
        verbose_name_plural: str = verbose_name
        proxy: bool = False
        abstract: bool = False
        get_latest_by: list[str] = [
            "date_joined",
            "is_active",
        ]
        ordering: list[str] = get_latest_by

    username_validator: UsernameValidator = UsernameValidator()
    USERNAME_FIELD: str = "username"  #: field for username
    REQUIRED_FIELDS: list[str] = []  #: required fields for model creation

    # model fields
    username: CharField = CharField(
        max_length=20,
        blank=False,
        null=False,
        unique=True,
        help_text=" ".join(
            [
                "usernames must be between 8 and 20 characters long",
                "and contain only",
                "letters, numbers, periods (.), and underscores (_)",
            ]
        ),
        validators=[username_validator],
    )
    is_staff: BooleanField = BooleanField(
        default=False, help_text="grants access to the admin site"
    )
    is_superuser: BooleanField = BooleanField(
        default=False, help_text="grants unrestricted access to everything"
    )
    is_active: BooleanField = BooleanField(
        default=True, help_text="grants login access"
    )
    is_of_age: BooleanField = BooleanField(
        default=False, help_text="is old enough to use the app"
    )
    date_joined: DateTimeField = DateTimeField(
        default=timezone.now,
        help_text="date and time the user was added to the site",
    )
    last_login: DateTimeField = DateTimeField(
        blank=True,
        null=True,
        verbose_name="last_login",
    )

    # model manager
    objects: CustomAccountManager = CustomAccountManager()

    # model methods
    def __str__(self) -> str:
        """__str__

        Returns the instance's username
        """
        return self.username

    def status(self) -> str:
        """status

        Returns:
            (str): the account status in a human-readable format
        """
        return get_bool(self.is_active)

    def get_slug(self) -> str:
        return self.username

    def get_absolute_url(self):
        return reverse("account-detail", kwargs={"slug": self.get_slug()})

    def save(self, *args, **kwargs) -> "CustomAccount":
        """save

        Overwrites the default save function to normalize the username
        and populate the slug field.
        """
        self.username = normalize_username(self.username)
        return super(CustomAccount, self).save(*args, **kwargs)
