"""Profile model."""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from utils.models import SpendTrackerModel


class MonthlyBill(SpendTrackerModel):
    """Monthly Bill model.
    A Monthly bill holds a transaction's repetition data like billing date.
    """

    transaction = models.OneToOneField(
        "transactions.Transaction", on_delete=models.CASCADE
    )
    billing_date = models.IntegerField(blank=False, validators=[
        MaxValueValidator(30),
        MinValueValidator(1)
    ])
