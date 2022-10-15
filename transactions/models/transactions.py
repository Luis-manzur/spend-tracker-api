"""Transaction model."""

from django.db import models

from utils.models import SpendTrackerModel


class Transaction(SpendTrackerModel):
    """Transaction model.
    An account holds a user's private and personal transaction data like amount, category, account
    and statistics.
    """

    CATEGORIES_CHOICES = (
        ("Food", "Food"),
        ("Gas", "Gas"),
        ("Investment", "Investment"),
        ("Other", "Other"),
        ("Entertainment", "Entertainment"),
        ("Insurance", "Insurance"),
        ("Groceries", "Groceries"),
        ("Gaming", "Gaming"),
        ("Education", "Education"),
        ("Fashion", "Fashion"),
        ("Transport", "Transport"),
        ("Personal", "Personal"),
        ("Housing", "Housing"),
        ("Debt", "Debt"),
        ("Rent", "Rent"),
        ("Salaries", "Salaries"),
        ("Income", "Income"),
        ("Time job", "Time job"),
        ("Bonus", "Bonus"),
        ("Wage", "Wage"),
        ("Tip", "Tip"),
    )

    TYPE_CHOICES = (("Income", "Income"), ("Expense", "Expense"))

    account = models.ForeignKey("accounts.Account", related_name='transactions', on_delete=models.CASCADE)

    name = models.CharField(" name", blank=False, max_length=120)

    description = models.CharField(max_length=120)

    category = models.CharField(choices=CATEGORIES_CHOICES, blank=False, max_length=20)

    amount = models.FloatField(
        "transaction amount",
        default=0,
        help_text="Balance summary from account.",
    )

    type = models.CharField(choices=TYPE_CHOICES, blank=False, max_length=20)

    def __str__(self):
        """Return Account name str."""
        return str(self.name)
