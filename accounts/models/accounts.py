"""Account model."""

# Django
from django.db import models

# Utilities
from utils.models import SpendTrackerModel


class Account(SpendTrackerModel):
    """Account model.
    An account holds a user's private and personal accounts data like name, balance, type
    and statistics.
    """

    TYPE_CHOICES = (
            ("Bank", "Bank"),
            ("Cash", "Cash"),
            ("Crypto", "Crypto"),
    )

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    name = models.CharField(
        "Account name", blank=False, max_length=120
    )
    type = models.CharField(choices=TYPE_CHOICES, blank=True, max_length=20)

    balance = models.FloatField(
        "Account Balance",
        default=0,
        help_text="Balance summary from account.",
    )

    def __str__(self):
        """Return Account name str."""
        return str(self.name)
