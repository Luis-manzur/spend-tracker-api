"""Account serializer."""

from rest_framework import serializers

from accounts.models import Account


class AccountModelSerializer(serializers.ModelSerializer):
    """Account model serializer."""

    class Meta:
        """Meta class."""

        model = Account
        fields = ("name", "type", "balance")
        read_only_fields = ("balance",)


class CreateAccountModelSerializer(serializers.ModelSerializer):
    """Create account model serializer."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        """Meta class."""

        model = Account
        exclude = ["is_active"]
