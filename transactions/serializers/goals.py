"""Goal serializer."""

from rest_framework import serializers

from accounts.models import Account
from transactions.models import Goal
from users.models import User


class GoalModelSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        exclude = ["is_active"]


class CreateGoalModelSerializer(serializers.ModelSerializer):
    use_current_savings = serializers.BooleanField(default=False)

    def validate_use_current_savings(self, data):
        try:
            if data:
                user: User = self.initial_data.get("user")
                accounts = Account.objects.filter(user=user)

                balance = 0
                for account in accounts:
                    balance += account.balance

                goal_amount = self.initial_data.get("amount")
                if balance >= goal_amount:
                    raise serializers.ValidationError(
                        "You already have your goal amount"
                    )
        except Exception as ex:
            raise serializers.ValidationError(f"Unexpected error occurred: {ex}")

        finally:
            return data

    class Meta:
        model = Goal
        exclude = ["is_active"]
