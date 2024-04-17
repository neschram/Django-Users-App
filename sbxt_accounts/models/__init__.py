# accounts/models/__init__.py
from .account_models import CustomAccountManager, CustomAccount
from .profile_models import AccountProfile

modules: list[str] = [
    CustomAccountManager.__doc__,
    CustomAccount.__doc__,
    AccountProfile.__doc__,
]
"""modules is a list of docstrings for each model"""

__doc__: str = str("\n".join(modules))
