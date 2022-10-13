"""Transaction serializer."""

from rest_framework import serializers

from accounts.models import Account
from transactions.models import Transaction


class TransactionModelSerializer(serializers.ModelSerializer):
    """Transaction model serializer."""

    class Meta:
        """Meta class."""

        model = Transaction
        fields = ("name", "type", "amount", "category")
        read_only_fields = ("amount", "type")


class CreateTransactionModelSerializer(serializers.ModelSerializer):
    """Create transaction model serializer."""

    class Meta:
        """Meta class."""

        model = Transaction
        exclude = ["is_active"]

    def validate_category(self, data):
        selected_type = self.initial_data["type"]
        income_categories = ["Income", "Time Job", "Bonus", "Wage", "Tip", "Salaries"]
        expense_categories = [
            "Food",
            "Gas",
            "Investment",
            "Other",
            "Entertainment",
            "Insurance",
            "Groceries",
            "Gaming",
            "Education",
            "Fashion",
            "Transport",
            "Personal",
            "Housing",
            "Debt",
            "Rent",
        ]

        if selected_type == "Expense" and data in income_categories:
            raise serializers.ValidationError(
                "The selected category doesn't qualify as an expense."
            )

        elif selected_type == "Income" and data in expense_categories:
            raise serializers.ValidationError(
                "The selected category doesn't qualify as an income."
            )

        return data

    def validate_amount(self, data):
        account = Account.objects.get(pk=self.initial_data["account"])
        self.context["account"] = account

        if self.initial_data["type"] == "Expense":

            if account.balance < data:
                raise serializers.ValidationError(
                    "The amount is greater than the actual amount."
                )

        return data

    def create(self, validated_data):
        # Update account Balance
        account = self.context["account"]

        if self.initial_data["type"] == "Income":
            account.balance += validated_data["amount"]

        else:
            account.balance -= validated_data["amount"]

        account.save()

        # Save transaction

        return super(CreateTransactionModelSerializer, self).create(validated_data)
