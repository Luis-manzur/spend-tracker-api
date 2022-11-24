from django.db import models

from users.models import User
from utils.models import SpendTrackerModel


class Debt(SpendTrackerModel):
    from_user = models.ForeignKey(
        User, related_name="from_user", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(User, related_name="to_user", on_delete=models.CASCADE)
    amount = models.FloatField(null=False, blank=False)

    STATUS = [("unpaid", "unpaid"), ("paid", "paid")]
    status = models.CharField(choices=STATUS, default="unpaid", max_length=17)
