# accounts/apps.py

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """AccountsConfig

    accounts app configuration
    """

    default_auto_field: str = "django.db.models.BigAutoField"
    """default database auto incrimenting field"""
    name: str = "sbxt_accounts"  #: app name
    verbose_name: str = "accounts"  #: app plural name
    label: str = "accounts"  #: app label
