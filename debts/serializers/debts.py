"""Debts Serializers"""
from rest_framework import serializers

from accounts.models import Account
from debts.models import Debt
from transactions.models import Transaction
from users.serializers import SimpleUserSerializer


class CreateDebtModelSerializer(serializers.ModelSerializer):
    from_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Debt
        fields = ["from_user", "to_user", "amount", "id"]

    def validate(self, data):
        if data["from_user"] == data["to_user"]:
            raise serializers.ValidationError("You can't create a debt to your self!")

        return data


class DebtModelSerializer(serializers.ModelSerializer):
    from_user = SimpleUserSerializer(read_only=True)
    to_user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Debt
        fields = ["from_user", "to_user", "amount", "id"]


class PayDebtModelSerializer(serializers.Serializer):
    debt_id = serializers.IntegerField()
    account = serializers.IntegerField()

    def validate_debt_id(self, data):
        try:
            debt = Debt.objects.get(pk=data)
            if not debt:
                raise serializers.ValidationError(
                    "This debt id did not match any debt!"
                )
            else:
                self.context["debt"] = debt

        except Exception as e:
            raise serializers.ValidationError(e)

        return data

    def validate_account(self, data):
        try:
            account = Account.objects.get(pk=data)
            if not account:
                raise serializers.ValidationError(
                    "This account id did not match any account!"
                )
            else:
                debt: Debt = self.context["debt"]
                if not debt:
                    raise serializers.ValidationError("The debt wasn't found")
                if account.balance < debt.amount:
                    raise serializers.ValidationError(
                        "This account doesn't have enough balance!"
                    )
                self.context["account"] = account

        except Exception as e:
            raise serializers.ValidationError(e)

        return data

    def create(self, validated_data):
        try:
            account: Account = self.context["account"]
            debt: Debt = self.context["debt"]
            transaction_description = f"debt payment to {account.user.username}"
            transaction_name = f"debt to {account.user.username}"
            transaction = Transaction.objects.create(
                account=account,
                category="Debt",
                type="Expense",
                description=transaction_description,
                amount=debt.amount,
                name=transaction_name,
            )
            account.balance -= debt.amount
            account.save()
            transaction.save()
            debt.delete()
        except Exception as e:
            raise serializers.ValidationError(f"Unexpected error '{e}'")
