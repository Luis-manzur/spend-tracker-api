"""Profile model."""

# Django
from django.db import models

# Utilities
from utils.models import SpendTrackerModel


class Profile(SpendTrackerModel):
    """Profile model.
    A profile holds a user's public data like biography, picture,
    and statistics.
    """

    user = models.OneToOneField("users.User", on_delete=models.CASCADE)

    picture = models.ImageField(
        "profile picture", upload_to="users/pictures/", blank=True, null=True
    )
    biography = models.TextField(max_length=500, blank=True)

    # Stats
    balance = models.FloatField(
        "Profile Balance",
        default=0,
        help_text="Balance summary from all user accounts.",
    )

    def __str__(self):
        """Return user's str representation."""
        return str(self.user)
