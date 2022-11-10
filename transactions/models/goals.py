"""Goal model."""
from django.core.validators import MinValueValidator
from django.db import models

from users.models import User
from utils.models import SpendTrackerModel


class Goal(SpendTrackerModel):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    name = models.CharField(null=False, blank=False, max_length=40)
    description = models.CharField(null=False, blank=False, max_length=250)
    amount = models.FloatField(null=False, validators=[
        MinValueValidator(1),
    ])
    saved = models.FloatField(null=False, default=0)
