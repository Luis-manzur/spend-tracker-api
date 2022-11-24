"""Debts Serializers"""
from rest_framework import serializers

from accounts.models import Account
from debts.models import Debt
from debts.tasks import send_debt_paid_email, send_debt_email
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

    def create(self, validated_data):
        debt = Debt.objects.create(**validated_data)
        debt.save()
        send_debt_email.delay(debt.pk)
        return debt


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
            transaction = Transaction.objects.create(
                account=account,
                category="Debt",
                type="Expense",
                description=f"debt payment to {debt.from_user.username}",
                amount=debt.amount,
                name=f"debt to {debt.from_user.username}",
            )
            account.balance -= debt.amount
            account.save()
            transaction.save()

            friend_account = Account.objects.filter(user=debt.from_user).first()

            friend_transaction = Transaction.objects.create(
                account=friend_account,
                category="Income",
                type="Income",
                description=f"debt from {debt.to_user.username}",
                amount=debt.amount,
                name=f"debt from {debt.to_user.username}",
            )
            friend_account.balance += debt.amount
            friend_account.save()
            friend_transaction.save()

            send_debt_paid_email.delay(debt.id)

            debt.delete()
        except Exception as e:
            raise serializers.ValidationError(f"Unexpected error '{e}'")
