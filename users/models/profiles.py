"""Profile model."""

from django.db import models

from utils.models import SpendTrackerModel


class Profile(SpendTrackerModel):
    """Profile model.
    A profile holds a user's public data like biography and picture.
    """

    MEMBERSHIPS = [("PREMIUM", "PREMIUM"), ("FREE", "FREE")]

    user = models.OneToOneField("users.User", on_delete=models.CASCADE)

    picture = models.ImageField(
        "profile picture", upload_to="users/pictures/", blank=True, null=True
    )
    biography = models.TextField(max_length=500, blank=True)

    membership = models.CharField(max_length=8, choices=MEMBERSHIPS, default="FREE")

    def __str__(self):
        """Return user's str representation."""
        return str(self.user)
