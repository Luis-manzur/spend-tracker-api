"""Account serializer."""

# Django REST Framework
from rest_framework import serializers

# Models
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
        fields = "__all__"
