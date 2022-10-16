"""Transaction serializer."""

from rest_framework import serializers

from accounts.models import Account
from transactions.models import Transaction, MonthlyBill
from transactions.serializers import MonthlyBillModelSerializer


class TransactionModelSerializer(serializers.ModelSerializer):
    """Transaction model serializer."""

    class Meta:
        """Meta class."""

        model = Transaction
        fields = ("name", "type", "amount", "category", "created")
        read_only_fields = ("amount", "type")


class CreateTransactionModelSerializer(serializers.ModelSerializer):
    """Create transaction model serializer."""
    monthlybill = MonthlyBillModelSerializer(required=False, allow_null=True, default=None)
    is_month_to_month = serializers.BooleanField(required=True)

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

    def validate_monthlybill(self, data):
        month_to_month = self.initial_data.get("is_month_to_month")

        if month_to_month and data is None:
            raise serializers.ValidationError("This field is required.")

        return data

    def create(self, validated_data):
        is_month_to_month = validated_data.get('is_month_to_month')
        monthly_bill = validated_data.get('monthlybill')

        if monthly_bill is not None:
            del validated_data['monthlybill']

        if is_month_to_month is not None:
            del validated_data['is_month_to_month']

        transaction = Transaction.objects.create(**validated_data)

        if not is_month_to_month:
            validated_data["monthlybill"] = None
            account = self.context["account"]

            if self.initial_data["type"] == "Income":
                account.balance += validated_data["amount"]

            else:
                account.balance -= validated_data["amount"]

            account.save()
        else:
            monthly_bill['transaction'] = transaction
            monthly_bill = MonthlyBill.objects.create(**monthly_bill)

        # Save transaction
        return transaction
