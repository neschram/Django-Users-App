# accounts/models/profile_models.py

from django.core.validators import EmailValidator
from django.db.models import (
    Model,
    CharField,
    TextField,
    SlugField,
    EmailField,
    BooleanField,
    OneToOneField,
    ImageField,
    CASCADE,
)
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from sbxt_accounts.utils import (
    user_profile_media,
    format_name,
)


class AccountProfile(Model):
    """AccountProfile

    Contains the personal information associated with a `CustomAccount` such as:
        - the user's first and last name
        - contact information
        - public view access
        - profile picture
    """

    class Meta:
        """Meta for AccountProfile"""

        db_table: str = "accounts_profiles"
        db_table_comment: str = "user profiles"
        managed: bool = True
        verbose_name: str = _("profiles")
        # additional options
        verbose_name_plural: str = verbose_name
        proxy: bool = False
        abstract: bool = False
        get_latest_by: list[str] = [
            "user__date_joined",
        ]
        ordering: list[str] = [
            "last_name",
            "first_name",
        ]

    slug: SlugField = SlugField(_("profile link"), blank=True)
    account: OneToOneField = OneToOneField(
        "sbxt_accounts.CustomAccount",
        to_field="username",
        related_name="account_profile",
        on_delete=CASCADE,
        primary_key=True,
    )  #: slug field for url
    first_name: CharField = CharField(
        _("first name"),
        max_length=50,
        blank=False,
    )  #: first name
    last_name: CharField = CharField(
        _("last name"),
        max_length=50,
        blank=False,
    )  #: last name
    email: EmailField = EmailField(
        _("email address"),
        max_length=254,
        validators=[EmailValidator],
        blank=False,
        unique=True,
    )  #: email address
    phone: PhoneNumberField = PhoneNumberField(
        _("phone number"),
        blank=True,
        help_text="please use international format. \n ex: +12223334444",
    )  # phone number
    is_public: BooleanField = BooleanField(
        _("profile is public"),
        default=False,
        help_text="check here to allow others to view your profile",
    )  #: public profile
    description: TextField = TextField(
        _("profile description"),
        max_length=1500,
        blank=True,
        null=True,
    )  #: profile description
    profile_pic: ImageField = ImageField(
        _("profile image"),
        upload_to=user_profile_media,
        default="accounts/profile_image.png",
        blank=True,
        null=True,
    )  #: profile picture

    def __str__(self) -> str:
        """__str__

        Returns:
            (str): the instance's username
        """
        return self.user.username

    def get_short_name(self) -> str:
        """get_short_name

        Get a shortend version of the user's full name

        Returns:
            (str): first_name[0] + last_name
        """
        fn: str = self.first_name[0].upper()
        ln: str = format_name(self.last_name)
        return f"{fn} {ln}"

    def get_full_name(self) -> str:
        """get_full_name

        Format the user's full name

        Returns:
            (str) format_name(self.first_name) + format_name(self.last_name)
        """

        fn: str = format_name(self.first_name)
        ln: str = format_name(self.last_name)
        return f"{fn} {ln}"

    get_full_name.short_description = "Name"

    def get_absolute_url(self) -> str:
        """get_absolute_url

        Returns the URL path to the profile
        """
        return reverse("profile-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs) -> "AccountProfile":
        self.slug = self.user.get_slug()
        return super(AccountProfile, self).save(*args, **kwargs)
