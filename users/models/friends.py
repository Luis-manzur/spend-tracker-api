from django.db import models

from users.models import User
from utils.models import SpendTrackerModel


class FriendRequest(SpendTrackerModel):
    from_user = models.ForeignKey(
        User, related_name="from_user", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(User, related_name="to_user", on_delete=models.CASCADE)
